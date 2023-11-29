import datetime
import importlib
import importlib.resources
import importlib.util
import io
import os
import re
import subprocess
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import pkg_resources
from packaging.utils import parse_sdist_filename, parse_wheel_filename
from radicli import Arg
from wasabi import msg

from .. import ty
from ..cli import cli
from ..errors import CLIError
from ..messages import Messages
from ..prodigy_teams_broker_sdk import errors as broker_errors
from ..prodigy_teams_broker_sdk.models import RecipesMeta
from ..prodigy_teams_pam_sdk import Client
from ..prodigy_teams_pam_sdk.models import PackageCreating, RecipeCreating
from ._state import get_auth_state


@dataclass
class DistPackage:
    """Package to publish, from a wheel, src directory or sdist path"""

    path: Path
    name: str
    version: str

    def __init__(self, path: Path) -> None:
        if path.suffix == ".whl":
            name, version, _, _2 = parse_wheel_filename(path.name)
        else:
            name, version = parse_sdist_filename(path.name)

        self.name = name.replace("-", "_").lower()
        self.version = str(version)
        self.path = path

    @property
    def versioned_name(self) -> str:
        return f"{self.name}-{self.version}"

    @property
    def filename(self) -> str:
        return self.path.name

    def get_bytes(self) -> bytes:
        with self.path.open("rb") as file_:
            data = file_.read()
        return data


@dataclass
class ModulePackage:
    """Package to publish, from an importable module."""

    name: str
    version: str

    def __init__(self, name: str, version_arg: Optional[str] = None) -> None:
        self.name = name
        if version_arg is None:
            utc_now = datetime.datetime.utcnow()
            self.version = f"{utc_now.year}.{utc_now.month}.{utc_now.day}-{utc_now.second+60*utc_now.minute+60*60*utc_now.hour}"
        else:
            self.version = version_arg

    @property
    def versioned_name(self) -> str:
        return f"{self.name}-{self.version}"

    @property
    def filename(self) -> str:
        return f"{self.versioned_name}.tar"

    @property
    def is_path(self) -> bool:
        return False

    def get_bytes(self) -> bytes:
        return _export_module_files(self.name)


@cli.subcommand(
    "publish",
    "code",
    name_or_path=Arg(help="Path or name of importable module with the recipes"),
    python_version=Arg(
        "--python-version",
        help="Which Python version to use for the remote environment",
    ),
    package_version=Arg("--package-version", help="Version identifier for the package"),
    requirements=Arg(
        "--requirements",
        short="-r",
        help="Path to requirements file. prodigy and prodigy_teams_recipes_sdk and added automatically if missing",
    ),
    deps=Arg(
        "--dep",
        short="-d",
        help="Path or name of importable module for dependencies to upload",
    ),
    # fmt: on
)
def publish_code(
    name_or_path: str,
    python_version: str = "3.9",
    package_version: ty.Optional[str] = None,
    requirements: ty.Optional[ty.Path] = None,
    deps: ty.List[Path] = [],
) -> ty.Optional[ty.UUID]:
    """
    Upload and advertise a recipes package from your Python environment.
    """
    auth = get_auth_state()
    if auth.broker_host is None:
        raise CLIError(Messages.E035)
    if auth.broker_id is None:
        raise CLIError(Messages.E036)

    if _is_path(name_or_path):
        package = DistPackage(_make_sdist_if_dir(Path(name_or_path)))
        contents = package.get_bytes()
    else:
        package = ModulePackage(name_or_path, package_version)
        msg.info("Getting package contents")
        contents = package.get_bytes()
        if package_version is None:
            msg.info(f"No version specified. Defaulting to {package.version}")
    if requirements is None:
        if isinstance(package, ModulePackage):
            msg.info("Finding requirements")
            requirements_str = _infer_requirements(package.name)
        else:
            requirements_str = None
    else:
        with requirements.open("r", encoding="utf8") as file_:
            requirements_str = file_.read()
        if isinstance(package, ModulePackage):
            requirements_str = _add_default_requirements(requirements_str)

    remote_path = f"{{__tmp__}}/{package.filename}"

    with msg.loading(f"Uploading {len(contents)} bytes to cluster"):
        try:
            auth.broker_client.files.upload(
                io.BytesIO(contents),
                dest=remote_path,
                overwrite=True,
                make_dirs=True,
            )
        except broker_errors.FileError as e:
            msg.fail(title="Error uploading to {remote_path}", text=str(e), exits=1)
    dep_paths = []
    for dep in deps:
        dep = _make_sdist_if_dir(dep)
        dep_path = f"{{__wheels__}}/{dep.name}"
        with dep.open("rb") as file_:
            try:
                auth.broker_client.files.upload(
                    file_, dest=dep_path, overwrite=True, make_dirs=True
                )
            except broker_errors.FileError as e:
                msg.fail(title=f"Error uploading to {dep_path}", text=str(e), exits=1)
        dep_paths.append(dep_path)
    with msg.loading("Starting env creation on the cluster"):
        r = auth.broker_client.envs.create(
            package_name=package.name,
            package_path=remote_path,
            package_version=package.version,
            python_version=python_version,
            requirements=requirements_str,
            deps=dep_paths,
            is_dist_package=isinstance(package, DistPackage),
        )
    if r.validation_error is not None:
        msg.fail(
            title="Internal error starting environment creation",
            text=(
                "The broker service failed to submit a valid task "
                "to the Nomad cluster. This is an internal error "
                "not caused by your input.\n"
                f"Error message: {r.validation_error.message}"
            ),
            spaced=True,
            exits=1,
        )
    elif r.nomad_error is not None:
        msg.fail(
            title="Cluster availability error starting environment creation",
            text=(
                f"The broker service could not submit the environment creation "
                f"task to the Nomad cluster.\n"
                f"Details of the request that failed on the cluster:\n"
                f"URL: {r.nomad_error.url}\n"
                f"Status code: {r.nomad_error.status_code}\n"
                f"Method: {r.nomad_error.method}\n"
                f"Body: {r.nomad_error.body}"
            ),
            spaced=True,
            exits=1,
        )
    elif r.status is None:
        msg.fail(
            title="Internal error starting environment creation",
            text="Invalid response from server: One of 'status', 'validation_error' or 'nomad_error' must be set.",
            spaced=True,
            exits=1,
        )
    status = r.status
    msg.good("Environment creation task submitted. Waiting for it to finish.")
    start = time.time()
    for message in auth.broker_client.jobs.messages(ty.UUID(status.job_id)):
        msg.info(message)
    elapsed = int(time.time() - start)
    msg.good(f"Environment creation complete after {elapsed}s")
    env_path = status.path
    metas = auth.broker_client.envs.get_recipes_meta(package.name, package.version)
    msg.info("Advertising package to PAM server")
    package_id = _publish_package_to_pam(
        auth.client,
        auth.broker_id,
        name=package.name,
        meta=metas,
        environment=env_path,
        filename=package.filename,
        version=package.version,
    )
    msg.good("Publication complete")
    return package_id


def _is_path(name_or_path: str) -> bool:
    try:
        Path(name_or_path)
    except ValueError:
        return False
    else:
        return True


def _make_sdist_if_dir(path: Path) -> ty.Path:
    if not path.is_dir():
        return path
    env = dict(os.environ)
    env["SKIP_CYTHON"] = "1"
    r = subprocess.run(["python", "setup.py", "sdist"], cwd=path, text=True, env=env)
    r.check_returncode()
    dists = list((path / "dist").iterdir())
    if len(dists) == 0:
        raise ValueError("sdist not created after subprocess in {path / 'dist'}")
    # Return last modified file
    return max(dists, key=lambda p: p.stat().st_mtime)


def _publish_package_to_pam(
    client: Client,
    broker_id: ty.UUID,
    *,
    name: str,
    filename: str,
    version: str,
    environment: str,
    meta: RecipesMeta,
) -> ty.UUID:
    msg.info(f"Creating package with {len(meta.recipes)} recipes")
    package = client.package.create(
        PackageCreating(
            name=name.replace("_", "-"),
            filename=filename,
            version=version,
            broker_id=broker_id,
            environment=environment,
            meta={r["name"]: r for r in meta.recipes},
        )
    )

    msg.good(
        Messages.T002.format(noun="package", name=f"{package.name} ({package.id})")
    )
    for recipe_data in meta.recipes:
        # The recipe create-meta command is supposed to output
        # entries that match the RecipeCreating body, except
        # for missing a package_id
        body = RecipeCreating(**recipe_data, package_id=package.id)
        r = client.recipe.create(body)
        recipe_type = "action" if body.is_action is True else "task"
        msg.good(Messages.T002.format(noun=f"{recipe_type} recipe", name=r.name))
    return package.id


def _export_module_files(module_name: str) -> bytes:
    module = importlib.import_module(module_name)
    assert not isinstance(module, str)
    assert module is not None
    assert module.__file__ is not None
    path = Path(module.__file__)

    dist_path = _get_dist_info_path(module_name)
    if dist_path is None:
        # Package isn't a distribution -- it's just on the path
        record = _get_module_sources(path)
    elif dist_path.name.endswith("egg-info"):
        # Package is an 'egg'. This happens most often from pip install -e
        record = _read_sources(dist_path / "SOURCES.txt")
    elif not (dist_path / "RECORD").exists():
        # I think ths means it's an editable install?
        record = _get_module_sources(path)
    else:
        # Package is a distribution. This happens when you've installed from a
        # wheel or sdist
        record = _read_record(dist_path / "RECORD")
    # Archive the files
    buf = io.BytesIO()
    with tarfile.open(f"{module_name}.tar", "w", fileobj=buf) as tar:
        for subpath in record:
            tar.add(path.parent.parent / Path(subpath), arcname=subpath)
    output_data = buf.getvalue()
    return output_data


def _get_module_sources(parent: Path) -> List[str]:
    if not parent.is_dir() and parent.name != "__init__.py":
        return [parent.name]
    elif not parent.is_dir():
        parent = parent.parent
    queue = [parent]
    output = []
    for path in queue:
        if path.name == "__pycache__":
            continue
        elif path.is_dir():
            queue.extend(path.iterdir())
        elif path.suffix == ".py":
            output.append(str(path.relative_to(parent.parent)))
    return output


def _get_dist_info_path(package_name: str) -> Optional[Path]:
    try:
        dist = pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        return None
    if dist.egg_info is None:
        return None
    else:
        return Path(dist.egg_info)


def _read_sources(path: Path) -> List[str]:
    with path.open("r", encoding="utf8") as file_:
        output = file_.read().strip().split("\n")
    return output


def _read_record(path: Path) -> List[str]:
    output = []
    with path.open("r", encoding="utf8") as file_:
        for line in file_.read().strip().split("\n"):
            subpath, sha, size = line.split(",")
            output.append(subpath)
    return output


def _infer_requirements(package_name: str) -> str:
    try:
        distribution = pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        return ""
    return "\n".join([str(r) for r in distribution.requires()])


def _add_default_requirements(requirements: str) -> str:
    if not re.search(r"prodigy[^\w_-]", requirements):
        # TODO: We'll want this to specify the download location, and then
        # have pip pull in the credentials from the environment.
        requirements += "\n# Default\nprodigy\n"
    if not re.search(r"prodigy_teams_recipes_sdk[^\w_]", requirements):
        requirements += "\n# Default\nprodigy_teams_recipes_sdk\n"
    return requirements

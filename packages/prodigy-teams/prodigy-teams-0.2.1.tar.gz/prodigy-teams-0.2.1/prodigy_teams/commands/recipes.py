import builtins
import json
import os
import re
import tarfile
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from packaging.version import Version
from radicli import Arg
from wasabi import msg

from .. import ty
from ..cli import cli
from ..errors import CLIError
from ..messages import Messages
from ..prodigy_teams_broker_sdk import Client as BrokerClient
from ..prodigy_teams_pam_sdk import Client
from ..prodigy_teams_pam_sdk.models import (
    PackageReading,
    RecipeDetail,
    RecipeListingLatest,
    RecipeSummary,
)
from ..query import resolve_recipe
from ..ui import dicts_to_table, print_info_table, print_table_with_select
from ._state import get_auth_state

COOKIECUTTER_PATH = Path(__file__).parent.parent / "recipes_cookiecutter"


@cli.subcommand(
    "recipes",
    "list",
    # fmt: off
    select=Arg("--select", help=Messages.select.format(opts=list(RecipeSummary.__fields__))),
    as_json=Arg("--json", help=Messages.as_json),
    # fmt: on
)
def list(
    select: ty.List[str] = ["id", "name"],
    as_json: bool = False,
) -> ty.Sequence[RecipeSummary]:
    """List all recipes"""
    auth = get_auth_state()
    # When there are multiple versions of a package publishing some recipe, only
    # list the latest version.
    res = auth.client.recipe.all_latest(
        body=RecipeListingLatest(broker_id=auth.broker_id, org_id=auth.org_id)
    )
    print_table_with_select(res.items, select=select, as_json=as_json)
    return res.items


@cli.subcommand(
    "recipes",
    "info",
    name_or_id=Arg(help=Messages.name_or_id.format(noun="recipe")),
    cluster_id=Arg(help=Messages.cluster_id.format(noun="recipe")),
    select=Arg(
        "--select",
        help=Messages.select.format(opts=builtins.list(RecipeDetail.__fields__)),
    ),
    as_json=Arg("--json", help=Messages.as_json),
)
def info(
    name_or_id: ty.StrOrUUID,
    cluster_id: ty.Optional[ty.UUID] = None,
    select: ty.Optional[ty.List[str]] = None,
    as_json: bool = False,
) -> RecipeDetail:
    """Show info about a recipe"""
    auth = get_auth_state()
    if cluster_id is None:
        cluster_id = auth.broker_id
    res = resolve_recipe(name_or_id, broker_id=cluster_id)
    print_info_table(res, as_json=as_json, select=select)
    return res


@cli.subcommand(
    "recipes",
    "init",
    # fmt: off
    output_dir=Arg(help=Messages.output_dir.format(noun="recipe package")),
    name=Arg("--name", help=Messages.name.format(noun="package (e.g. custom_recipes)")),
    version=Arg("--version", help=Messages.version.format(noun="package")),
    description=Arg("--description", help=Messages.description.format(noun="package")),
    author=Arg("--author", help=Messages.name.format(noun="package author")),
    email=Arg("--email", help=Messages.email.format(noun="package author")),
    url=Arg("--url", help=Messages.url.format(noun="package")),
    license=Arg("--license", help=Messages.license.format(noun="package")),
    # fmt: on
)
def init(
    output_dir: Path,
    name: ty.Optional[str] = None,
    version: str = "0.1.0",
    description: str = "",
    author: str = "",
    email: str = "",
    url: str = "",
    license: str = "",
) -> None:
    """Generate a new recipes Python package"""
    # output_dir is passed as the path to the package itself, but our template
    # structure includes the package directory under the `package_dir` key.
    package_dir = output_dir.resolve()
    parent_dir = package_dir.parent.resolve()
    package_dir = package_dir.name
    # Infer a default package name from the directory path
    name = name or package_dir
    # Create a wheel-friendly package name slug
    package_name = re.sub(r"[^\w\d.]+", "_", name.lower(), re.UNICODE)
    template_dir = COOKIECUTTER_PATH
    variables = {
        "name": name,  # human friendly recipe package name
        "version": version,
        "short_description": description,
        "author": author,
        "email": email,
        "url": url,
        "license": license,
        "parent_dir": str(parent_dir),  # the directory path containing the package
        "package_dir": package_dir,  # top-level package directory within `parent_dir`
        "package_name": package_name,  # the normalized name of the package
    }
    if not _ensure_preconditions(template_dir, variables):
        msg.info(Messages.E154.format(name=name))
        return None
    _fill_template(template_dir, variables)
    msg.good(Messages.T002.format(noun="package", name=name), str(output_dir))


# TDOO: this needs to be part of the publish command
# @cli.subcommand(
#     "recipes",
#     "verify",
#     package=Arg(help=Messages.path.format(noun="package")),
# )
def verify(package: ty.ExistingFilePath) -> None:
    """Verify a built recipe package before upload"""
    if not (package.name.endswith("tar.gz") or package.name.endswith(".whl")):
        raise CLIError(Messages.E144, package.name)
    file_name = ""
    meta_json = None
    valid_meta = False
    if package.name.endswith(".whl"):
        with ZipFile(package) as zip_file:
            for file_name in zip_file.namelist():
                if file_name.endswith("/meta.json"):
                    meta_bytes = zip_file.read(file_name)
                    meta_json = json.loads(meta_bytes.decode("utf-8"))
                    if not isinstance(meta_json, dict):
                        continue
                    if "prodigy_teams" in meta_json:
                        valid_meta = True
                        break
    elif package.name.endswith(".tar.gz"):
        with tarfile.open(package) as tar:
            for file_name in tar.getnames():
                if file_name.endswith("/meta.json"):
                    io_bytes = tar.extractfile(file_name)
                    assert io_bytes
                    meta_json = json.load(io_bytes)
                    if not isinstance(meta_json, dict):
                        continue
                    if "prodigy_teams" in meta_json:
                        valid_meta = True
                        break
    if not (valid_meta and meta_json):
        raise CLIError(Messages.E145)
    msg.good(Messages.T022, file_name)
    recipes_data = meta_json.get("prodigy_teams", {}).get("recipes")
    if not isinstance(recipes_data, dict):
        raise CLIError(Messages.E146, recipes_data)
    if not recipes_data:
        raise CLIError(Messages.E147, Messages.E148)
    recipes_info = []
    invalid_recipes = []
    for key, data in recipes_data.items():
        entry_point = data.get("entry_point")
        recipe_args = data.get("args")
        data = {
            "name": key,
            "entry_point": entry_point,
            "contains args": bool(recipe_args),
        }
        recipes_info.append(data)
        if not entry_point or not recipe_args:
            invalid_recipes.append(key)
    headers, rows = dicts_to_table(recipes_info)
    msg.good(Messages.T023)
    msg.table(rows, header=headers, divider=True, max_col=3000)
    if invalid_recipes:
        raise CLIError(Messages.E149, ", ".join(invalid_recipes))
    msg.good(Messages.T024)


def _check_for_package(
    client: Client, broker_id: ty.UUID, distribution_name: str, version: Version
) -> ty.Tuple[bool, ty.List[Version]]:
    packages = client.package.all(
        PackageReading(
            broker_id=broker_id,
            filename=None,
            name=distribution_name,
            version=None,
            id=None,
            org_id=None,
        )
    )
    published_versions = [Version(p.version) for p in packages.items]
    exists = any(v == version for v in published_versions)
    return exists, published_versions


def _upload_wheels(client: BrokerClient, srcs: ty.List[Path], dest: str) -> None:
    for src in srcs:
        with src.open("rb") as file_:
            client.files.upload(
                file_,
                dest=os.path.join(dest, src.name),
                make_dirs=True,
                overwrite=True,
            )
            msg.good(Messages.T033.format(src=src.name))


def _ensure_preconditions(template_dir: Path, variables: ty.Dict[str, ty.Any]) -> bool:
    output_dir = Path(variables["parent_dir"])
    if output_dir.exists() and output_dir.is_file():
        msg.fail(Messages.E002.format(noun="directory", name=str(output_dir)))
        return False
    conflicts = _find_overwrite_conflicts(template_dir, variables)
    if conflicts:
        for conflict_file in conflicts:
            msg.fail(Messages.E002.format(noun="file", name=str(conflict_file)))
        return False
    return True


def _find_overwrite_conflicts(
    template_dir: Path, variables: ty.Dict[str, ty.Any]
) -> ty.List[ty.Union[Path, "TemplateItem"]]:
    output_dir = Path(variables["parent_dir"])
    conflicts = []
    if output_dir.exists() and output_dir.is_dir():
        for tmpl in _walk_template(template_dir):
            out_file = tmpl.output_path(variables)
            if out_file.exists():
                conflicts.append(out_file)
    elif output_dir.exists() and output_dir.is_file():
        conflicts.append(output_dir)
    return conflicts


@dataclass
class TemplateItem:
    template_dir: Path
    template_path: Path

    def output_path(self, variables: ty.Dict[str, ty.Any]) -> Path:
        return Path(variables["parent_dir"]) / _replace_path_vars(
            self.template_path.relative_to(self.template_dir), variables
        )

    def expand(self, variables: ty.Dict[str, ty.Any]) -> str:
        with self.template_path.open("r", encoding="utf8") as file_:
            return _replace_content_vars(file_.read(), variables)


def _fill_template(template_dir: Path, variables: ty.Dict[str, ty.Any]) -> None:
    # TODO: check cookiecutter.json for defaults?
    for tmpl in _walk_template(template_dir):
        if tmpl.template_path.suffix == ".pyc":
            continue

        contents = tmpl.expand(variables)
        output_path = tmpl.output_path(variables)
        if output_path.name.endswith(".tmpl"):
            # We allow files to be named *.thing.tmpl to denote that it's a template
            # of a .thing file, but not currently a valid .thing file. We still might
            # replace variables in files named other things, if the variable substitution
            # doesn't change the syntactic validity of the file. So if we have a .tmpl
            # suffix, we just strip that.
            output_path = output_path.parent / output_path.name[: -len(".tmpl")]
        output_path.parent.mkdir(exist_ok=True, parents=True)
        with output_path.open("w", encoding="utf8") as file_:
            file_.write(contents)


def _replace_content_vars(
    contents: str,
    variables: ty.Dict[str, ty.Any],
    *,
    var_prefix="{{cookiecutter.",
    var_suffix="}}",
) -> str:
    for key, value in variables.items():
        key = f"{var_prefix}{key}{var_suffix}"
        contents = contents.replace(key, value)
    return contents


def _replace_path_vars(
    path: Path,
    variables: ty.Dict[str, ty.Any],
    *,
    var_prefix="{{cookiecutter.",
    var_suffix="}}",
) -> Path:
    """Given a path that might have variables, fill in the variables
    from a given dict.
    """
    parts = []
    for part in path.parts:
        if part.startswith(var_prefix) and part.endswith(var_suffix):
            variable = part[len(var_prefix) : -len(var_suffix)]
            part = variables[variable]
        parts.append(part)
    if not parts:
        return path
    else:
        return Path(parts[0]).joinpath(*parts[1:])


def _walk_template(template_dir: Path) -> ty.Iterable[TemplateItem]:
    def _walk(path: Path) -> ty.Iterable[Path]:
        for p in Path(path).iterdir():
            if p.is_dir():
                yield from _walk(p)
                continue
            if p.name == "cookiecutter.json":
                continue
            yield p

    for p in _walk(template_dir):
        yield TemplateItem(template_dir, p)

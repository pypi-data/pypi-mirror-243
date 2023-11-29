import json
from pathlib import Path

from radicli import Arg

from .. import ty
from ..cli import cli
from ..errors import CLIError
from ..messages import Messages
from . import assets as assets_commands
from . import files as files_commands
from ._state import get_auth_state


@cli.subcommand(
    "publish",
    "data",
    src=Arg(help="File or directory to publish"),
    dest=Arg(help="Destination path to copy the data to"),
    name=Arg("--name", help=Messages.name.format(noun="asset")),
    version=Arg("--version", help=Messages.version.format(noun="asset")),
    kind=Arg(
        "--kind",
        help=Messages.asset_kind,
    ),
    loader=Arg("--loader", help="Loader to convert data for Prodigy"),
    meta=Arg("--meta", help=Messages.asset_meta),
    exists_ok=Arg("--exists-ok", help=Messages.exists_ok),
    # fmt: on
)
def publish_data(
    src: Path,
    kind: str,
    dest: ty.Optional[str] = None,
    name: ty.Optional[str] = None,
    version: ty.Optional[str] = None,
    loader: ty.Optional[str] = None,
    meta: str = "{}",
    exists_ok: bool = False,
) -> ty.Optional[ty.UUID]:
    """
    Transfer data to the cluster, and advertise it to Prodigy Teams.

    These steps can also be done separately. See `ptc files` to transfer
    data to the cluster without creating an Asset record for it, and
    `ptc assets create` to create an Asset without transfer.
    """
    auth = get_auth_state()
    if auth.broker_host is None:
        raise CLIError(Messages.E035)
    if auth.broker_id is None:
        raise CLIError(Messages.E036)

    if name is None:
        name = src.name
    if dest is None:
        if version is None:
            filename = name
        else:
            filename = f"{name}-{version}"
        dest = f"{{__nfs__}}/data/{filename}"
    if loader is not None:
        meta_json = json.loads(meta)
        meta_json.update({"loader": loader})
        meta = json.dumps(meta_json)
    if version is None:
        version = "0.0.0"

    files_commands.cp(
        str(src),
        dest=dest,
        overwrite=True,
        make_dirs=True,
        recurse=True,
        cluster_host=auth.broker_host,
    )
    assets_commands.create(
        kind=kind,
        name=name,
        path=dest,
        version=version,
        meta=meta,
        exists_ok=exists_ok,
    )
    # TODO: We should also have an option to create a dataset
    # from the asset, by triggering a 'db-in' action.

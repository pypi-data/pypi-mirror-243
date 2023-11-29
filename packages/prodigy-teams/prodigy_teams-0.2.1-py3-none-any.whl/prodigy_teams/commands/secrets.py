import builtins
from getpass import getpass

from radicli import Arg
from wasabi import msg

from .. import ty
from ..cli import cli
from ..errors import CLIError, ProdigyTeamsErrors
from ..messages import Messages
from ..prodigy_teams_broker_sdk.models import Secret
from ..prodigy_teams_pam_sdk.models import SecretDetail, SecretSummary
from ..query import resolve_secret
from ..ui import print_info_table, print_table_with_select
from ._state import get_auth_state


@cli.subcommand(
    "secrets",
    "list",
    # fmt: off
    select=Arg("--select", help=Messages.select.format(opts=list(SecretSummary.__fields__))),
    as_json=Arg("--json", help=Messages.as_json),
    # fmt: on
)
def list(
    select: ty.List[str] = ["created", "id", "name", "path"], as_json: bool = False
) -> ty.Sequence[SecretSummary]:
    """List all named pointers to secrets on the cluster"""
    client = get_auth_state().client
    res = client.secret.all()
    print_table_with_select(res.items, select=select, as_json=as_json)
    return res.items


@cli.subcommand(
    "secrets",
    "info",
    name_or_id=Arg(help=Messages.name_or_id.format(noun="secret")),
    cluster_id=Arg(help=Messages.cluster_id.format(noun="secret")),
    select=Arg(
        "--select",
        help=Messages.select.format(opts=builtins.list(SecretDetail.__fields__)),
    ),
    as_json=Arg("--json", help=Messages.as_json),
)
def info(
    name_or_id: ty.StrOrUUID,
    cluster_id: ty.Optional[ty.UUID] = None,
    select: ty.Optional[ty.List[str]] = None,
    as_json: bool = False,
) -> SecretDetail:
    """Show info about a secret on the cluster"""
    res = resolve_secret(name_or_id, broker_id=cluster_id)
    print_info_table(res, as_json=as_json, select=select)
    return res


@cli.subcommand_with_extra(
    "secrets",
    "create",
    name=Arg(help=Messages.name.format(noun="secret name")),
    secrets_path=Arg("--secrets-path", help=Messages.secrets_path),
    exists_ok=Arg("--exists-ok", help=Messages.exists_ok),
)
def create(
    name: str, _extra: ty.List[str], secrets_path: str = "/", exists_ok: bool = False
) -> ty.Optional[ty.UUID]:
    """Create a named pointer to a secret on the cluster"""
    auth = get_auth_state()
    client = auth.client
    broker_client = auth.broker_client
    broker_id = auth.broker_id

    secret_dict = {}
    for arg in _extra:
        if "=" not in arg:
            raise CLIError(Messages.E056)
        else:
            key, value = arg.split("=", 1)
            if value == "-":
                editor_value = getpass(f"Enter secret value for {key}: ")
                secret_dict[key] = editor_value
            else:
                secret_dict[key] = value

    if not secret_dict:
        raise CLIError(Messages.E057)

    key_prefix = secrets_path.strip("/")
    key = name
    if key_prefix:
        key = f"{key_prefix}/{name}"
    broker_secret = Secret(key=key, value=secret_dict)
    broker_client.secrets.create(broker_secret)

    try:
        res = client.secret.create(name=name, path=secrets_path, broker_id=broker_id)
    except ProdigyTeamsErrors.SecretExists:
        if exists_ok:
            msg.info(Messages.T001.format(noun="secret", name=name))
            return None
        raise CLIError(Messages.E002.format(noun="secret", name=name))
    except ProdigyTeamsErrors.SecretInvalid:
        raise CLIError(Messages.E004.format(noun="secret", name=name))
    except ProdigyTeamsErrors.SecretForbiddenCreate:
        raise CLIError(Messages.E003.format(noun="secret", name=name))
    msg.divider("Secret")
    msg.table(res.dict())
    return res.id


@cli.subcommand(
    "secrets",
    "delete",
    name_or_id=Arg(help=Messages.name_or_id.format(noun="secret")),
    cluster_id=Arg(help=Messages.cluster_id.format(noun="secret")),
)
def delete(
    name_or_id: ty.StrOrUUID, cluster_id: ty.Optional[ty.UUID] = None
) -> ty.UUID:
    """Delete a secret by name or ID"""

    auth = get_auth_state()
    client = auth.client
    broker_client = auth.broker_client
    cluster_id = cluster_id or auth.broker_id

    pam_secret = resolve_secret(name_or_id, broker_id=cluster_id)
    broker_client.secrets.delete(key=pam_secret.name)

    try:
        client.secret.delete(id=pam_secret.id)
    except (
        ProdigyTeamsErrors.SecretForbiddenDelete,
        ProdigyTeamsErrors.SecretNotFound,
    ):
        raise CLIError(Messages.E006.format(noun="secret", name=name_or_id))
    else:
        msg.good(Messages.T003.format(noun="secret", name=name_or_id))
    return pam_secret.id

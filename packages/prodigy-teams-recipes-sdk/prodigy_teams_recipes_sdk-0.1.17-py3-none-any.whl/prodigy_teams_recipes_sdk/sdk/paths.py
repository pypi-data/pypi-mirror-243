import posixpath
import re
from typing import Optional, Tuple, cast
from uuid import UUID

from ..prodigy_teams_pam_sdk import models as pam_models
from ..prodigy_teams_pam_sdk.recipe_client import Client

# Place this close to the function for convenience.
# TODO: This will have trouble with escaped curlies right?
_PATH_RE = re.compile(r"^(?:\{(\w+)\}:)?(?:\{(\w+)\}/?)?([^{}]*)$")


def _parse_remote_path(path: str) -> Tuple[Optional[str], Optional[str], str]:
    match_obj = _PATH_RE.match(path)
    if match_obj is None:
        raise ValueError(f"Cannot parse path {path}")
    groups = match_obj.groups()
    if len(groups) != 3:
        raise ValueError(f"Cannot parse path {path}")
    return groups


def _resolve_remote_path(
    client: Client, remote: str, broker_id: UUID
) -> Tuple[Optional[pam_models.BrokerPathSummary], str, str]:
    path_parts = _parse_remote_path(remote)
    if path_parts[1] is None:
        return None, path_parts[2], path_parts[2]
    _, path_name, subpath = path_parts
    query = pam_models.BrokerPathReading(
        broker_id=broker_id,
        name=path_name,
        id=None,
        path=None,
    )
    result = cast(pam_models.BrokerPathSummary, client.broker_path.read(query))
    # These paths should always be treated as unix paths since they are remote.
    # Some consumers may also expect trailing slashes to be preserved.
    joined = posixpath.join(result.path, subpath)
    return result, subpath, joined


def resolve_remote_path(client: Client, remote: str, broker_id: UUID) -> str:
    _, _, joined = _resolve_remote_path(client, remote, broker_id)
    return joined

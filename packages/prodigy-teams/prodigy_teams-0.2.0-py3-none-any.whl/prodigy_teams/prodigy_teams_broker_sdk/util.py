import json

import httpcore
import httpx

from . import ty


def nomad_stream(
    *,
    client: httpx.Client,
    url: str,
    method: str,
    index: int,
    params: ty.Optional[ty.Dict[str, ty.Any]] = None,
    timeout: ty.Optional[int],
) -> ty.Iterable[dict]:
    """Stream from Nomad, reconnecting when disconnected."""
    if params is None:
        params = {}
    if index <= 0:
        index = -1
    while True:
        with client.stream(
            url=url,
            method=method,
            params={"index": index + 1}.update(params),
            timeout=timeout,
        ) as response:
            try:
                for line in response.iter_lines():
                    events = json.loads(line)
                    if events is None:
                        return
                    yield events
                    if "Index" in events:
                        index = max(events["Index"], index)
            except (
                httpcore.ReadTimeout,
                httpx.ReadTimeout,
                httpx.RemoteProtocolError,
                httpx.WriteError,
                httpx.WriteTimeout,
            ):
                continue


async def nomad_stream_async(
    *,
    client: httpx.AsyncClient,
    url: str,
    method: str,
    index: int,
    timeout: ty.Optional[int],
    params: ty.Optional[ty.Dict[str, ty.Any]] = None,
) -> ty.AsyncIterable[dict]:
    """Stream from Nomad asynchronously, reconnecting when disconnected."""
    if params is None:
        params = {}
    if index <= 0:
        index = -1
    while True:
        async with client.stream(
            url=url,
            method=method,
            params={"index": index + 1}.update(params),
            timeout=timeout,
        ) as response:
            try:
                async for line in response.aiter_lines():
                    events = json.loads(line)
                    if events is None:
                        return
                    yield events
                    if "Index" in events:
                        index = max(events["Index"], index)
            except (
                httpcore.ReadTimeout,
                httpx.ReadTimeout,
                httpx.RemoteProtocolError,
                httpx.WriteError,
                httpx.WriteTimeout,
            ):
                continue


__all__ = ["nomad_stream", "nomad_stream_async"]

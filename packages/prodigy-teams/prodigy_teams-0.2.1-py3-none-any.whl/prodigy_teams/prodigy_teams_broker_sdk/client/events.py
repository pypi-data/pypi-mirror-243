from .. import ty
from ..util import nomad_stream, nomad_stream_async
from .base import BaseClient


class Events(BaseClient):
    def stream(
        self,
        topics: ty.List[str],
        namespace: str = "default",
        index: int = 0,
        timeout: int = 600,
    ) -> ty.Iterable[dict]:
        for item in nomad_stream(
            client=self._sync_client,
            method="GET",
            url="/api/v1/events/stream",
            params={"topics": topics, "namespace": namespace},
            index=index,
            timeout=timeout,
        ):
            yield item

    async def stream_async(
        self,
        topics: ty.List[str],
        namespace: str = "default",
        index: int = 0,
        timeout: int = 600,
    ) -> ty.AsyncIterable[dict]:
        async for item in nomad_stream_async(
            client=self._async_client,
            method="GET",
            url="/api/v1/events/stream",
            params={"topics": topics, "namespace": namespace},
            index=index,
            timeout=timeout,
        ):
            yield item

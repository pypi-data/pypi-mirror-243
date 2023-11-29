from .. import ty
from ..models import Secret, SecretResponse
from .base import BaseClient


class SecretClient(BaseClient):
    def create(self, secret: Secret) -> bool:
        res = self.request("POST", endpoint="create", data=secret)
        return ty.cast(bool, res)

    async def create_async(self, secret: Secret) -> bool:
        res = await self.request_async("POST", endpoint="create", data=secret)
        return ty.cast(bool, res)

    def read(self, key: str) -> ty.List[SecretResponse]:
        res = self.request(
            "POST",
            endpoint="read",
            data={"key": key},
            return_model=ty.List[SecretResponse],
        )
        return ty.cast(ty.List[SecretResponse], res)

    async def read_async(self, key: str) -> ty.List[SecretResponse]:
        res = await self.request_async(
            "POST",
            endpoint="read",
            data={"key": key},
            return_model=ty.List[SecretResponse],
        )
        return ty.cast(ty.List[SecretResponse], res)

    def delete(self, key: str) -> bool:
        res = self.request("POST", endpoint="delete", data={"key": key})
        return ty.cast(bool, res)

    async def delete_async(self, key: str) -> bool:
        res = await self.request_async("POST", endpoint="delete", data={"key": key})
        return ty.cast(bool, res)

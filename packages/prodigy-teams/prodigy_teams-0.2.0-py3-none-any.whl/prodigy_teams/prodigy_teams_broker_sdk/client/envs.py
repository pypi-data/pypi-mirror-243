import httpx

from .. import ty
from ..models import (
    EnvCreate,
    EnvCreateResponse,
    EnvCreateStatus,
    RecipesMeta,
    Requirement,
)
from .base import BaseClient


class Envs(BaseClient):
    def create(
        self,
        *,
        is_dist_package: bool,
        package_name: str,
        package_version: str,
        python_version: str,
        package_path: str,
        requirements: ty.Optional[ty.Union[str, ty.List[Requirement]]] = None,
        deps: ty.List[str] = [],
    ) -> EnvCreateResponse:
        res = self.request(
            "POST",
            endpoint=f"{package_name}/{package_version}/{python_version}",
            data=EnvCreate(
                is_dist_package=is_dist_package,
                package_path=str(package_path),
                requirements_txt=requirements
                if isinstance(requirements, str)
                else None,
                requirements=requirements if isinstance(requirements, list) else None,
                deps=list(deps),
            ),
            return_model=EnvCreateResponse,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvCreateResponse, res)

    async def create_async(
        self,
        *,
        is_dist_package: bool,
        package_name: str,
        package_version: str,
        python_version: str,
        package_path: str,
        requirements: ty.Optional[ty.Union[str, ty.List[Requirement]]] = None,
        deps: ty.List[str] = [],
    ) -> EnvCreateResponse:
        res = self.request_async(
            "POST",
            endpoint=f"{package_name}/{package_version}/{python_version}",
            data=EnvCreate(
                is_dist_package=is_dist_package,
                package_path=str(package_path),
                requirements_txt=requirements
                if isinstance(requirements, str)
                else None,
                requirements=requirements if isinstance(requirements, list) else None,
                deps=deps,
            ),
            return_model=EnvCreateResponse,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvCreateResponse, res)

    def check_status(
        self,
        package_name: str,
        package_version: str,
        python_version: str,
        job_id: ty.UUID,
        alloc_id: ty.Optional[ty.UUID] = None,
        eval_id: ty.Optional[ty.UUID] = None,
    ) -> EnvCreateStatus:
        res = self.request(
            "GET",
            endpoint=f"{package_name}/{package_version}/{python_version}/{job_id}",
            params={"alloc_id": alloc_id, "eval_id": eval_id},
            return_model=EnvCreateStatus,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvCreateStatus, res)

    async def check_status_async(
        self,
        package_name: str,
        package_version: str,
        python_version: str,
        job_id: ty.UUID,
        alloc_id: ty.Optional[ty.UUID] = None,
        eval_id: ty.Optional[ty.UUID] = None,
    ) -> EnvCreateStatus:
        res = await self.request_async(
            "GET",
            endpoint=f"{package_name}/{package_version}/{python_version}/{job_id}",
            params={"alloc_id": alloc_id, "eval_id": eval_id},
            return_model=EnvCreateStatus,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvCreateStatus, res)

    def get_recipes_meta(self, package_name: str, package_version: str) -> RecipesMeta:
        res = self.request(
            "GET",
            endpoint=f"{package_name}/{package_version}/meta",
            return_model=RecipesMeta,
        )
        return ty.cast(RecipesMeta, res)

    async def get_recipes_meta_async(
        self, package_name: str, package_version: str
    ) -> RecipesMeta:
        res = await self.request_async(
            "GET",
            endpoint=f"{package_name}/{package_version}/meta",
            return_model=RecipesMeta,
        )
        return ty.cast(RecipesMeta, res)

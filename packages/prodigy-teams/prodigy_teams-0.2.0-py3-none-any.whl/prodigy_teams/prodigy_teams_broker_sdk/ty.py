from typing import (
    IO,
    Any,
    AsyncIterable,
    AsyncIterator,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    NamedTuple,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from pydantic import BaseModel, conint
from pydantic.generics import GenericModel

T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: conint(ge=1)  # type: ignore
    size: conint(ge=1)  # type: ignore


__all__ = [
    "Any",
    "AsyncIterator",
    "AsyncIterable",
    "BaseModel",
    "cast",
    "Dict",
    "IO",
    "Iterable",
    "Iterator",
    "List",
    "Literal",
    "NamedTuple",
    "Optional",
    "Type",
    "Union",
    "UUID",
]

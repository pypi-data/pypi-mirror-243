from __future__ import annotations

import functools
from abc import abstractmethod, ABCMeta
from typing import (
    Any,
    Self,
    TypeVar,
    Generic,
    SupportsIndex,
    overload,
    Callable,
)

from bs4.element import Tag

from .full_dunder import FullDunder

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)


class BroadcastList(list[T]):
    @property
    def bc(self) -> _BroadcastedList[T]:
        return _BroadcastedList(self)


class _BroadcastedList(FullDunder, Generic[T_co]):
    def _callable_attr_broadcast(self, *args, **kwargs) -> BroadcastList:
        __attr_name = kwargs.pop("__attr_name")
        return BroadcastList(getattr(i, __attr_name)(*args, **kwargs) for i in self._broadcastlist_value)

    def __init__(self, broadcastlist: BroadcastList[T_co]) -> None:
        self._broadcastlist_value = broadcastlist

    def __getattr__(self, __name: str) -> Callable[..., BroadcastList] | BroadcastList:
        if not self._broadcastlist_value:
            return self._broadcastlist_value

        if callable(getattr(self._broadcastlist_value[0], __name)):
            return functools.partial(self._callable_attr_broadcast, __attr_name=__name)

        return BroadcastList(getattr(i, __name) for i in self._broadcastlist_value)

    def _callable_dunder_getattr(self, __name: str, *args, **kwargs) -> Any:
        # print(__name, args, kwargs)
        return self.__getattr__(__name)(*args, **kwargs)  # type: ignore

    async def _callable_dunder_getattr_async(self, __name: str, *args, **kwargs) -> Any:
        return await self.__getattr__(__name)(*args, **kwargs)  # type: ignore

    def __setattr__(self, name: str, value) -> None:
        if name == "_broadcastlist_value":
            return object.__setattr__(self, name, value)
        super().__setattr__(value)

    def __str__(self) -> str:
        return list.__str__(self._broadcastlist_value)


class NewTagBroadcastList(BroadcastList[Tag]):
    @property
    def bc(self) -> _TagBroadcastedList:
        return _TagBroadcastedList(self)  # type: ignore


class _TagBroadcastedList(_BroadcastedList[Tag]):
    """Chaining BroadcastED list especially for Tags."""


#########################
# LEGACY BROADCAST LIST #
#########################


class AbstractBroadcastList(list[T], metaclass=ABCMeta):
    @abstractmethod
    def _callable_attr_broadcast(self, *args, __attr_name: str | None = None, **kwargs) -> Any:
        ...

    @abstractmethod
    def _attr_broadcast(self, attr_name: str) -> Any:
        ...

    def __getattr__(self, __name: str):
        if __name.startswith('E'):
            __name = __name.removeprefix('E')

        # every element contained in list are assumed to be share same type.
        if callable(getattr(self[0], __name)):
            return functools.partial(self._callable_attr_broadcast, __attr_name=__name)
        else:
            return self._attr_broadcast(__name)


class NonchainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, __attr_name: str | None = None, **kwargs):
        if __attr_name is None:
            raise ValueError('__attr_name is empty. This function not intended to use outside of class.')
        return [getattr(i, __attr_name)(*args, **kwargs) for i in self]

    def _attr_broadcast(self, attr_name: str):
        return [getattr(i, attr_name) for i in self]

    @overload
    def __getitem__(self, __item: SupportsIndex) -> T:
        ...

    @overload
    def __getitem__(self, __item: slice) -> list[T]:
        ...

    @overload
    def __getitem__(self, __item) -> list:
        ...

    def __getitem__(self, __item) -> T | list[T] | list:
        """받은 값이 string인 경우 broadcasting하지만, 아니라면 리스트의 방법에 따릅니다.
        예를 들어 `thislist[0]`이나 `thislist[:4]`는 리스트의 메소드이지만,
        `thislist['src']`는 브로드캐스트됩니다."""
        if isinstance(__item, (SupportsIndex, slice)):
            return super().__getitem__(__item)

        return getattr(self, 'E__getitem__')(__item)


class ChainingBroadcastList(AbstractBroadcastList[T]):
    def _callable_attr_broadcast(self, *args, __attr_name: str | None = None, **kwargs):
        if __attr_name is None:
            raise ValueError('__attr_name is empty. This function not intended to use outside of class.')
        return ChainingBroadcastList([getattr(i, __attr_name)(*args, **kwargs) for i in self])

    def _attr_broadcast(self, attr_name: str):
        return ChainingBroadcastList([getattr(i, attr_name) for i in self])

    @overload
    def __getitem__(self, __item: SupportsIndex) -> T:
        ...

    @overload
    def __getitem__(self, __item: slice) -> Self:
        ...

    @overload
    def __getitem__(self, __item) -> ChainingBroadcastList:
        ...

    def __getitem__(self, __item) -> T | Self | ChainingBroadcastList:
        """받은 값이 string인 경우 broadcasting하지만, 아니라면 리스트의 방법에 따릅니다.
        예를 들어 `thislist[0]`이나 `thislist[:4]`는 리스트의 메소드이지만,
        `thislist['src']`는 브로드캐스트됩니다."""
        if isinstance(__item, SupportsIndex):
            return super().__getitem__(__item)
        if isinstance(__item, slice):
            return ChainingBroadcastList(super().__getitem__(__item))

        return getattr(self, 'E__getitem__')(__item)


class TagBroadcastList(ChainingBroadcastList[Tag]):
    """Chaining Broadcast list especially for Tags."""

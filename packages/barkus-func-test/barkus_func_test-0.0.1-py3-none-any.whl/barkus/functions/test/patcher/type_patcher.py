from unittest.mock import Mock
from typing import overload, Any, TypeVar, Tuple
from dataclasses import dataclass

_T = TypeVar("_T")

class TypePatcher:
    @overload
    def __call__(  # type: ignore[misc]
        self,
        target: str,
        new: _T,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> _T: ...
    @overload
    def __call__(
        self,
        target: str,
        *,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> Mock: ...
    @overload
    @staticmethod
    def object(  # type: ignore[misc]
        target: Any,
        attribute: str,
        new: _T,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> _T: ...
    @overload
    @staticmethod
    def object(
        target: Any,
        attribute: str,
        *,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> Any: ...
    @staticmethod
    def multiple(
        target: Any,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> Any: ...
    @staticmethod
    def stopall() -> None: ...

class Mocker:
    patch: TypePatcher

@dataclass
class PatcherCtx:
    location: str
    mocker: Mocker

    @staticmethod
    def resolve_mocker(mockerOrCtx, location: str|None) -> Tuple[Mocker, str|None]:
        if isinstance(mockerOrCtx, PatcherCtx):
            return (mockerOrCtx.mocker, mockerOrCtx.location or location)
        return (mockerOrCtx, location)

class BasePatcher:
    __location__: str|None = None

    def post_init(self, ctx: PatcherCtx):
        pass

    def __init__(self, mockerOrCtx, location: str|None = None):
        mocker, location = PatcherCtx.resolve_mocker(mockerOrCtx, location)
        if self.__location__ is None:
            if not location:
                raise Exception(f"Patcher - location not set | {self}")
            self.__location__ = location
        self.__ctx = PatcherCtx(location = str(self.__location__), mocker = mocker)
        self.post_init(self.__ctx)
        
    @overload
    def patch(  # type: ignore[misc]
        self,
        target: str,
        new: _T,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> _T: ...
    @overload
    def patch(
        self,
        target: str,
        *,
        spec: Any | None = ...,
        create: bool = ...,
        spec_set: Any | None = ...,
        autospec: Any | None = ...,
        new_callable: Any | None = ...,
        **kwargs: Any,
    ) -> Mock: ...

    def patch(self, target: str, *args: Any, **kwargs: Any) -> Any:
        mock: Any = self.__ctx.mocker.patch(f"{self.__location__}.{target}", *args, **kwargs)
        return mock

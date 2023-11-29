from typing import Any
from unittest.mock import Mock
from .context import PatcherCtx

class BasePatcher:
    __location__: str|None = None
    
    class Context(PatcherCtx):
        pass

    def setup(self, ctx: PatcherCtx):
        pass

    def __init__(self, mockerOrCtx, location: str|None = None):
        mocker, location = PatcherCtx.resolve_mocker(mockerOrCtx, location)
        if self.__location__ is None:
            if not location:
                raise Exception(f"Patcher - location not set | {self}")
            self.__location__ = location
        self.__ctx = PatcherCtx(location = str(self.__location__), mocker = mocker)
        self.setup(self.__ctx)
        
    def patch(self, target: str, *args: Any, **kwargs: Any) -> Mock:
        mock: Any = self.__ctx.mocker.patch(f"{self.__location__}.{target}", *args, **kwargs)
        return mock
    




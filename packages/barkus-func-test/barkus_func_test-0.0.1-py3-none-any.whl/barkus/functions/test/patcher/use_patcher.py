import pytest
from typing import TypeVar, Type, Generic
from .base_patcher import BasePatcher

_Patcher = TypeVar("_Patcher", bound = BasePatcher)

class UsePatcher(Generic[_Patcher]):
    __patcher__: Type[_Patcher]
    mocks: _Patcher

    @pytest.fixture(autouse = True)
    def setup_patcher_cls_mocks(self, mocker):
        self.mocks = self.__patcher__(mocker)
        yield
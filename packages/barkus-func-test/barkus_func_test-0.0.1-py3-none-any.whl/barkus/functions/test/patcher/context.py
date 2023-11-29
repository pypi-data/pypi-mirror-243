from typing import Tuple
from dataclasses import dataclass
from .type_patcher import TypePatcher

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


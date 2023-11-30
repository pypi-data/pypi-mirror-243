from dataclasses import dataclass

from .interfaces import _iSize


@dataclass(frozen=True)
class Blank(_iSize):
    _width: int
    _height: int

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

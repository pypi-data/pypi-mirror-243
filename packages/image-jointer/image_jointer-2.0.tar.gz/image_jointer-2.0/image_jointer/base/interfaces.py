from abc import ABC, abstractproperty


class _iSize(ABC):
    @abstractproperty
    def width(self) -> int:
        pass

    @abstractproperty
    def height(self) -> int:
        pass

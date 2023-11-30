from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: int = 0
    y: int = 0

    def __add__(self, other) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError(f"unsupported operand type: {type(self)} and {type(other)}")

        return Vector(self.x + other.x, self.y + other.y)

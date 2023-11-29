from __future__ import annotations

__all__ = ("Payload",)

from string import ascii_letters
from string import digits


class Payload:
    __slots__ = ("_bucket",)

    def __init__(self) -> None:
        self._bucket = sorted(set(x for x in f"{ascii_letters}{digits}"))

    def get(self) -> str:
        return self._bucket.pop()

    def put(self, value: str) -> None:
        self._bucket.append(value)
        self._bucket = sorted(set(self._bucket))

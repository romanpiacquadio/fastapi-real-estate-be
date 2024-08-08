from __future__ import annotations

from .submod import rand_gen
from .calculator import double

def main_func(num: int) -> dict[str, int]:
    d = rand_gen(num)
    return d


def my_double(number: float) -> float:
    return double(number)

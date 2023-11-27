"""
The functions in this module can be used in "if statements"
"""
from typing import (
    Iterable,
    Any
)
__all__ = [
    'excepting',
]


def excepting(other_than: Any, judg_target: Iterable) -> bool:
    return any(item != other_than for item in judg_target)

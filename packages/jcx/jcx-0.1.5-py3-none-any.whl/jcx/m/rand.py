from random import shuffle
from typing import Optional, Any


def random_choices(arr: list[Any], n: int, excluded: Optional[Any] = None) -> list[Any]:
    """数组中选出指定数量的其他元素"""
    arr1 = list(arr)
    if excluded is not None:
        arr1 = [a for a in arr1 if a != excluded]
    shuffle(arr1)
    n = min(n, len(arr1))
    return arr1[:n]

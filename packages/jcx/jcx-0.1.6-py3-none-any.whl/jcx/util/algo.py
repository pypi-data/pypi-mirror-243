from typing import Any

from rustshed import Option, Some, Null, to_option


def lookup(indexes: list, tab: list) -> list:
    """从表中查出所有索引对应的值"""
    return [tab[i] for i in indexes]


def dict_first_key(d: dict, value) -> Option[Any]:
    """字典中查找值对应的第一个键"""
    for k, v in d.items():
        if v == value:
            return Some(k)

    return Null


def low_pos(arr: list, value):
    """查找最小的插入位置"""
    for i, v in enumerate(arr):
        if value <= v:
            return i
    return len(arr)


def up_pos(arr: list, value):
    """查找最大的插入位置"""
    for i, v in enumerate(arr):
        if value < v:
            return i
    return len(arr)


@to_option
def list_index(arr: list, value) -> int:
    """List中查找值的索引，失败则Null"""
    return arr.index(value)

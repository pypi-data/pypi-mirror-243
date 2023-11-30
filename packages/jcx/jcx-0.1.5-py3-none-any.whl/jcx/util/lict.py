from dataclasses import dataclass
from typing import TypeVar, Generic, Mapping, Iterator, Optional, TypeAlias

KT = TypeVar('KT')
VT = TypeVar('VT')


@dataclass
class LictItem(Generic[KT, VT]):
    """Lict条目"""
    key: KT  # 键
    value: VT  # 值


LictItems: TypeAlias = list[LictItem[KT, VT]]
"""Lict条目数组"""


class LictIter(Iterator[KT]):
    """Lict迭代器"""

    def __init__(self, items: list[LictItem[KT, VT]]):
        self._items = items
        self._idx = -1

    def __next__(self) -> KT:
        self._idx += 1
        if self._idx < len(self._items):
            return self._items[self._idx].key
        raise StopIteration


class Lict(Mapping[KT, VT]):
    """列表字典, 受某种限制(如: flask_restx), 必须用list实现map功能"""

    def __init__(self, items: list[LictItem[KT, VT]]):
        self._items = items

    def inner(self) -> list[LictItem[KT, VT]]:
        """获取内部表示"""
        return self._items

    def index(self, key: KT) -> int:
        """获取 key 所在索引"""
        for i, item in enumerate(self._items):
            if item.key == key:
                return i
        return -1

    def __getitem__(self, key: KT) -> VT:
        """获取 key 对应的值"""
        i = self.index(key)
        if i > -1:
            return self._items[i].value
        raise KeyError(f'Key {key} not found.')

    def __setitem__(self, key: KT, value: VT):
        """获取 key 对应的值"""
        i = self.index(key)
        if i > -1:
            self._items[i].value = value
        self._items.append(LictItem[KT, VT](key, value))

    def pop(self, key, default_value=None) -> Optional[VT]:
        """删除 key 对应的值, 并返回"""
        i = self.index(key)
        if i > -1:
            return self._items.pop(i).value
        return default_value

    def __iter__(self) -> Iterator[KT]:
        return LictIter(self._items)

    def __len__(self) -> int:
        """获取元素数量"""
        return len(self._items)

    def to_dict(self) -> dict[KT, VT]:
        """转化成普通字典"""
        return {p.key: p.value for p in self._items}

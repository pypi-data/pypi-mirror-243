from typing import Iterator

from jcx.db.ivariant import IVariant


class Counter(Iterator[int]):
    """数据库计数器"""

    def __next__(self) -> int:
        """获取下一个数值"""
        v = self.get() + 1
        self.__var.set(v)
        return v

    def __init__(self, var: IVariant):
        self.__var = var

    def name(self) -> str:
        """"获取计数器名"""
        return self.__var.name()

    def get(self) -> int:
        """获取当前数值"""
        return self.__var.get() or 0

    def reset(self) -> None:
        """重置ID初值"""
        self.__var.set(0)

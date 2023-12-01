from typing import TypeVar, TypeAlias, Callable, Type

from pydantic import BaseModel, TypeAdapter

Self = TypeVar('Self', bound='Record')


class Record(BaseModel):
    """数据库记录"""
    id: int
    """记录ID"""

    def clone(self: Self) -> Self:
        """克隆记录"""
        return self.model_copy(deep=True)


RecordFilter: TypeAlias = Callable[[Record], bool]
"""记录过滤器"""

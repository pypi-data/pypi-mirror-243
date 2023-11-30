from abc import ABC
from pathlib import Path
from typing import TypeVar, Type, Optional

from cattr import unstructure, structure
from flask_restx import Resource  # type: ignore
from jcx.db.jdb.variant import JdbVariant
from jcx.db.record import PRecord

R = TypeVar("R", bound=PRecord)


class ItemDao(ABC):
    """条目数据访问对象"""

    def __init__(self, record_type: Type[R], folder: Path, name: str):
        self._var = JdbVariant(record_type, folder, name)

    def value_type(self) -> Type[R]:
        """获取条目类型"""
        return self._var.value_type()

    def variant(self):
        """获取数据变量"""
        return self._var

    def get(self) -> Optional[R]:
        """获取指定记录"""
        r: R = self._var.get()
        return r

    def update(self, r) -> Optional[R]:
        """更新记录"""
        r0: R = self._var.get()
        r = self.before_update(r, r0)
        if not r:
            return r
        self._var.set(r)
        self.after_update(r)
        return r

    def before_update(self, r: R, r0: R) -> Optional[R]:
        """更新记录之前的检查，可修改r值"""
        return r

    def after_update(self, r: R) -> None:
        """更新记录之后的检查，不可修改r值"""
        pass


def make_item(api, data: dict, item_type: Type[R]) -> tuple[bool, R]:
    """从数据构建条目"""
    try:
        item = structure(data, item_type)
    except TypeError as e:
        return False, api.abort(400, str(e))
    return True, item


def add_item_resource(ns, url, dao: ItemDao, model):
    """添加独立资源"""

    # TODO: model 通过 record_type 动态生成

    @ns.route(url)
    class Item(Resource):
        """展示所有条目列表，允许创建新条目"""

        @ns.doc('get_item')
        @ns.marshal_with(model)
        def get(self):
            """获取条目"""
            r = dao.get()
            return unstructure(r)

        @ns.expect(model)
        @ns.marshal_with(model)
        def put(self):
            """修改条目"""
            ok, r = make_item(self.api, self.api.payload, dao.value_type())
            if not ok:
                return r
            r = unstructure(dao.update(r))
            if not r:
                return self.api.abort(400, "更新条目失败")
            return r, 201

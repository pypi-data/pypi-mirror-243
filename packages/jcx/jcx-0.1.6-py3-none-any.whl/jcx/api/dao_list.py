from abc import ABC
from typing import TypeVar, Type, Optional

from cattr import unstructure, structure
from flask_restx import Resource  # type: ignore
from jcx.db.jdb.table import Table
from jcx.db.record import PRecord
from jcx.sys.fs import StrPath

R = TypeVar("R", bound=PRecord)


class ItemListDao(ABC):
    """条目集合数据访问对象"""

    def __init__(self, record_type: Type[R], folder: StrPath):
        self._tab = Table.open(record_type, folder)

    def record_type(self) -> Type[R]:
        """获取记录类型"""
        return self._tab.record_type()

    def table(self) -> Table:
        """获取数据表"""
        return self._tab

    def records(self) -> list[R]:
        """获取所有记录"""
        return self._tab.records()

    def get(self, rid: int) -> Optional[R]:
        """获取指定记录"""
        r = self._tab.get(rid)
        return r

    def add(self, record: R) -> Optional[R]:
        """添加新记录"""
        r = self.before_add(record)
        if r is None:
            return r

        record = self._tab.add(r)
        self.after_add(record)
        return record

    def update(self, record: R) -> Optional[R]:
        """更新记录"""
        r = self.before_update(record)
        if not r:
            return r
        record = self._tab.update(r).unwrap()
        self.after_update(record)
        return record

    def remove(self, record_id: int):
        """删除记录"""
        rid = self.before_remove(record_id)
        if not rid:
            return
        self._tab.remove(rid)
        self.after_remove(rid)

    def before_add(self, record: R) -> Optional[R]:
        """添加新记录之前的检查"""
        return record

    def before_update(self, record: R) -> Optional[R]:
        """更新记录之前的检查"""
        return record

    def before_remove(self, rid: int) -> Optional[int]:
        """删除记录之前的检查"""
        assert self
        return rid

    def after_add(self, record: R):
        """添加新记录之后的检查"""
        pass

    def after_update(self, record: R):
        """更新记录之后的检查"""
        pass

    def after_remove(self, rid: int):
        """删除记录之后的检查"""
        pass


def make_record(api, data: dict, record_type: Type[R], id: int = 0) -> tuple[bool, R]:
    """从数据构建记录"""
    if 'id' not in data:
        data['id'] = id
    try:
        r = structure(data, record_type)
    except TypeError as e:
        return False, api.abort(400, str(e))
    return True, r


def add_list_resource(ns, url, dao: ItemListDao, model):
    """添加集合资源"""

    # TODO: model 通过 record_type 动态生成

    @ns.route(url)
    class ItemList(Resource):
        """展示所有条目列表，允许创建新条目"""

        @ns.doc('list_items')
        @ns.marshal_list_with(model)
        def get(self):
            """列出所有条目"""
            rs = dao.records()
            return list(map(unstructure, rs))

        @ns.doc('create_item')
        @ns.expect(model)
        @ns.marshal_with(model, code=201)
        def post(self):
            """创建一个新条目"""
            ok, r = make_record(self.api, self.api.payload, dao.record_type())
            if not ok:
                return r
            r = unstructure(dao.add(r))
            if not r:
                return self.api.abort(400, "创建条目失败")
            return r, 201

    @ns.route(url + '/<int:id>')
    @ns.response(404, '指定条目未找到')
    @ns.param('id', '条目ID')
    class Item(Resource):
        """展示一个单独的条目，并允许修改和删除"""

        @ns.doc('get_item')
        @ns.marshal_with(model)
        def get(self, id):
            """获取指定条目"""
            r = unstructure(dao.get(id))
            return r or self.api.abort(404, "条目 %d 不存在" % id)

        @ns.doc('delete_item')
        @ns.response(204, '条目已经删除')
        def delete(self, id):
            """删除指定ID的条目"""
            dao.remove(id)
            return '', 204

        @ns.expect(model)
        @ns.marshal_with(model)
        def put(self, id):
            """修改指定ID的条目"""
            ok, r = make_record(self.api, self.api.payload, dao.record_type(), id)
            if not ok:
                return r
            if r.id != id:
                return self.api.abort(422, "数据中ID于URL中ID不符")
            r = unstructure(dao.update(r))
            if not r:
                return self.api.abort(400, "更新条目失败")
            return r, 201

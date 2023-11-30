from typing import TypeVar, Type

from jcx.db.rdb.db import RedisDb, DbCfg

T = TypeVar("T")


class RedisVariant:
    """数据库变量"""

    @staticmethod
    def open(value_type, db: RedisDb, name: str, default=None):
        """打开数据变量"""
        return RedisVariant(value_type, db, name, default)

    def __init__(self, value_type: Type[T], db: RedisDb, name: str, default=None):
        self._type = value_type
        self._db = db
        self._name = str(name)
        self._default = default

    def name(self):
        """"获取变量名"""
        return self._name

    def value_type(self):
        """"获取变量类型"""
        return self._type

    def exists(self):
        """"判断是否存在"""
        return self._db.exists(self._name)

    def get(self):
        """获取变量"""
        return self._db.get(self._name, self._type, self._default)

    def set(self, value):
        """设置变量"""
        self._db.set(self._name, value)

    def remove(self):
        """删除变量"""
        self._db.remove(self._name)


def a_test():
    db_cfg = DbCfg('redis://127.0.0.1/10')

    db = RedisDb(db_cfg.hot_db)

    name = RedisVariant(str, db, 'name')
    name.set('jack')
    v = name.get()
    print(v, type(v))

    age = RedisVariant(int, db, 'age')
    age.set(18)
    v = age.get()
    print(v, type(v))

    cfg = RedisVariant(DbCfg, db, 'cfg')
    cfg.set(db_cfg)
    v = cfg.get()
    print(v, type(v))

    print(cfg.exists())
    cfg.remove()
    print(cfg.exists())

    cfg = RedisVariant(DbCfg, db, 'cfg1', 0)
    v = cfg.get()
    print(v, type(v))


if __name__ == '__main__':
    a_test()

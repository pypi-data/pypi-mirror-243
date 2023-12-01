import re
from dataclasses import dataclass
from typing import TypeVar, Type, Any
from urllib.parse import urlparse

import redis
from jcx.text.txt_json import to_json, from_json

T = TypeVar("T")


@dataclass
class DbCfg:
    hot_db: str
    pretty: bool = True


class RedisDb:
    """数据库变量"""

    @staticmethod
    def open(server_url: str) -> 'RedisDb':
        """打开数据变量"""
        return RedisDb(server_url)

    def __init__(self, url: str):
        uri = urlparse(url)
        assert uri.scheme == 'redis'
        port = uri.port or 6379

        p = re.compile(r"/(\d+)")
        m = p.match(uri.path)
        assert m
        db_num = int(m.groups()[0])
        # print(db_num)
        self._name = str(db_num)
        self._db = redis.Redis(host=uri.hostname, port=port, db=db_num, decode_responses=True)

    def name(self) -> str:
        """"获取数据库名"""
        return self._name

    def set(self, name: str, value: Any) -> None:
        """保存变量"""
        self._db.set(name, to_json(value))

    def get(self, name: str, var_type: Type[T], default_value: T) -> T:
        """获取变量"""
        s = self._db.get(name)
        if not s:
            return default_value
        return from_json(s, var_type)

    def exists(self, name: str) -> bool:
        """"判断是否存在"""
        return self._db.exists(name) > 0

    def remove(self, name: str):
        """"删除"""
        self._db.delete(name)


def a_test() -> None:
    cfg = DbCfg('redis://127.0.0.1/10')

    db = RedisDb(cfg.hot_db)

    db.set('name', 'jack')
    v = db.get('name', str, '')
    print(v, type(v))

    db.set('age', 18)
    v = db.get('age', int, 0)
    print(v, type(v))

    db.set('cfg', cfg)
    v = db.get('cfg', DbCfg, DbCfg())
    print(v, type(v))

    print(db.exists('cfg'))
    db.remove('cfg')
    print(db.exists('cfg'))


if __name__ == '__main__':
    a_test()

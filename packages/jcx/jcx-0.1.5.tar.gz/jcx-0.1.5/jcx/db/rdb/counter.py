from jcx.db.counter import Counter
from jcx.db.rdb.db import RedisDb, DbCfg
from jcx.db.rdb.variant import RedisVariant


class RedisCounter(Counter):
    """Redis计数器"""

    def __init__(self, db: RedisDb, name: str):
        super().__init__(RedisVariant(int, db, name))


def test_counter() -> None:
    db_cfg = DbCfg('redis://127.0.0.1/10')

    db = RedisDb(db_cfg.hot_db)

    c1 = RedisCounter(db, 'test_c1')
    c1.reset()
    assert c1.get() == 0

    for i in range(1, 10):
        n = next(c1)
        assert i == n


if __name__ == '__main__':
    test_counter()

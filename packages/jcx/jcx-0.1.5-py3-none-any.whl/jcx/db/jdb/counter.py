from pathlib import Path

from jcx.db.counter import Counter
from jcx.db.jdb.variant import JdbVariant


class JdbCounter(Counter):
    """Jdb计数器"""

    def __init__(self, db: Path, name: str):
        super().__init__(JdbVariant(int, db, name))

from pathlib import Path
from typing import TypeVar, Type

from jcx.db.jdb.util import load_dict
from jcx.db.record import Record, RecordFilter
from jcx.rs.rs import rs_option_cloned
from jcx.sys.fs import rm_files_in, StrPath
from jcx.text.txt_json import save_json
from rustshed import Option, Null, Some

R = TypeVar("R", bound=Record)
"""记录类型"""


class Table:
    """数据库表"""

    @staticmethod
    def open(record_type: Type[R], folder: StrPath) -> 'Table':
        """打开数据库表"""
        tab = Table(record_type)
        tab.load(folder)
        return tab

    def __init__(self, record_type: Type[R]):
        self._type = record_type
        self._folder: Option[Path] = Null
        self._records: dict[int, R] = {}

    def load(self, folder: StrPath) -> int:
        """加载数据库表"""
        folder1 = Path(folder)
        folder1.mkdir(exist_ok=True)

        self._folder = Some(folder1)
        self._records = load_dict(self._type, folder)
        return len(self._records)

    def record_type(self) -> Type[R]:
        """获取记录类型"""
        return self._type

    def __len__(self) -> int:
        return len(self._records)

    def ids(self) -> list[int]:
        """获取所有ID"""
        return list(self._records.keys())

    def records(self) -> list[R]:
        """获取所有记录，防止被外部导致磁盘数据不一致"""
        return sorted(self._records.values(), key=lambda r: r.id)

    def get(self, rid: int) -> Option[R]:
        """获取指定记录"""
        r = self._records.get(rid)
        return rs_option_cloned(r)

    def query(self, fun: RecordFilter) -> list[R]:
        """查询满足条件的记录集"""
        return [r for r in self._records.values() if fun(r)]

    def query_ids(self, fun: RecordFilter) -> list[int]:
        """查询满足条件的记录ID集"""
        return [r.id for r in self._records.values() if fun(r)]

    def add(self, record: R) -> Option[R]:
        """添加新记录"""
        if record.id in self._records:
            return Null

        record = record.clone()  # 避免影响传入对象
        if record.id < 1:
            record.id = self.next_id()

        return self.update(record)

    def update(self, record: R) -> Option[R]:
        """更新记录"""
        if record.id < 1:
            return Null
        record = record.clone()  # 避免影响传入对象
        self._records[record.id] = record
        self.__save(record)
        return Some(record.clone())

    def remove(self, rid: int) -> None:
        """更新记录"""
        if rid not in self._records:
            return
        f = self.__record_path(rid)
        f.unlink()
        self._records.pop(rid)

    def clear(self) -> None:
        """删除所有记录"""
        self._records.clear()
        rm_files_in(self._folder.unwrap(), '.json')

    def next_id(self) -> int:
        """获取下一个ID"""
        return max(self.ids(), default=0) + 1

    def __record_path(self, rid: int) -> Path:
        """获取记录对应路径"""
        return self._folder.unwrap() / f'{rid}.json'

    def __save(self, record: R) -> None:
        """保存路径"""
        f = self.__record_path(record.id)
        save_json(record, f)

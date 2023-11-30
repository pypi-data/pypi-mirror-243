from pathlib import Path
from typing import TypeVar, Type, Optional

from jcx.db.record import Record, RecordFilter
from jcx.sys.fs import StrPath
from jcx.text.txt_json import load_json

R = TypeVar("R", bound=Record)


def load_list(record_type: Type[R], folder: StrPath, filter_: Optional[RecordFilter] = None) -> list[R]:
    """加载记录到列表"""
    records: list[R] = []

    folder = Path(folder)
    if not folder.is_dir():
        return records

    for f in folder.glob('*.json'):
        r = load_json(f, record_type).unwrap()
        if filter_ and not filter_(r):
            continue
        records.append(r)
    return records


def load_dict(record_type: Type[R], folder: StrPath, filter_: Optional[RecordFilter] = None) -> dict[int, R]:
    """加载记录到字典"""
    rs = load_list(record_type, folder, filter_)
    return {r.id: r for r in rs}

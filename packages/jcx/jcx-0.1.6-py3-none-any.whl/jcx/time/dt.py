import arrow
from arrow import Arrow

"""
参考：https://zhuanlan.zhihu.com/p/37164491
"""


def now_iso_str() -> str:
    """当前时间转字符串"""
    return datetime_iso_str(arrow.now())


def datetime_iso_str(dt: Arrow) -> str:
    """datetime转字符串"""
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '+08:00'


def iso_to_local(iso_str: str) -> str:
    """iso格式转本地表示"""
    dt = arrow.get(iso_str)
    return datetime_local_str(dt)


def datetime_local_str(dt: Arrow, ms: bool = False) -> str:
    """datetime转字符串"""
    n = 9 if ms else 13
    return str(dt)[:-n]


def now_local_str(ms: bool = False) -> str:
    """当前时间转字符串"""
    return datetime_local_str(arrow.now(), ms)


def now_id(ms: bool = False) -> str:
    """当前时间转ID"""
    s = now_local_str(ms)
    s = s.replace(' ', '_')
    s = s.replace('T', '_')
    s = s.replace(':', '-')
    return s


def now_file(ext: str = '', ms: bool = False) -> str:
    """当前时间转字作为文件名"""
    s = now_id(ms)
    return s + ext

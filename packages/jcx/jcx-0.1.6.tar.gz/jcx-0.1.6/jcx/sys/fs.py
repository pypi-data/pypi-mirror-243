import os
import re
import shutil
import sys
from enum import Enum
from pathlib import Path
from typing import TypeAlias, Generator, Any, Callable, Optional

import arrow
import sh  # type: ignore
from arrow import Arrow
from loguru import logger
from parse import parse  # type: ignore
from rustshed import Err, Result, Ok, Option, Some, Null

Paths: TypeAlias = list[Path]
"""路径数组"""

StrPath: TypeAlias = str | Path
"""路径表示：str或者Path"""

StrPaths: TypeAlias = list[StrPath]
"""可表示路径类型的数组"""


class Order(Enum):
    ASC = 1
    DESC = 2


def first_file_in(folders: StrPaths, file_name: str) -> Option[Path]:
    """从一组目录中查找指定文件，只获取第一个"""
    for p in folders:
        f = Path(p) / file_name
        if f.is_file():
            return Some(f)
    return Null


def files_in(folder: StrPath, ext: str, reverse: bool = False) -> list[Path]:
    """获取文件夹内指定扩展名的文件，有序"""
    p = Path(folder)
    return sorted(p.glob('*' + ext), reverse=reverse)


def file_names_in(folder: StrPath, ext: str, reverse: bool = False) -> list[str]:
    """获取文件夹内指定扩展名的文件名称，有序"""
    return [f.name for f in files_in(folder, ext, reverse)]


def find(src: StrPath, ext: str, order: Order = Order.ASC) -> list[Path]:
    """查找文件或文件夹内指定扩展名文件"""
    src = Path(src)
    if src.is_dir():
        files = sorted(src.rglob('*' + ext), reverse=(order == Order.DESC))
    elif src.is_file():
        files = [src]
    else:
        files = []
    return files


def find_first(folder: StrPath, pattern: str, recursive: bool = True) -> Result[Path, str]:
    """在文件夹内查找满足条件的第一个文件"""
    folder = Path(folder)
    if not folder.is_dir():
        return Err('指定路径不是目录: ' + str(folder))

    it = folder.rglob(pattern) if recursive else folder.glob(pattern)
    try:
        f = next(it)
    except StopIteration:
        return Err('指定文件找不到: ' + pattern)
    return Ok(f)


def find_in_parts(folder: StrPath, sub_path: str) -> Option[Path]:
    """在路径的各个部分里查找指定路径"""
    folder = Path(folder).absolute()
    while True:
        path = folder / sub_path
        if path.exists():
            return Some(path)
        folder = folder.parent
        if folder == folder.parent:
            break
    return Null


def file_exist_in(folder: StrPath, pattern: str, recursive: bool = False) -> bool:
    """判定目录中是否存在指定扩展名的文件"""
    return find_first(folder, pattern, recursive).is_ok()


def dirs_in(folder: StrPath, order: Order = Order.ASC) -> list[Path]:
    """获取文件夹"""
    folder = Path(folder)
    dirs: Paths = []
    if not folder.is_dir():
        return dirs
    for f in folder.iterdir():
        if f.is_dir():
            dirs.append(f)
    if order:
        return sorted(dirs, reverse=(order == Order.DESC))
    return dirs


def find_descendants(folder: StrPath, pattern: str, generation: int) -> list[Path]:
    """查找匹配模式的指定代子孙文件/目录"""
    assert generation > 0
    folder = Path(folder)

    if generation == 1:
        return sorted(folder.glob(pattern))

    children = dirs_in(folder)
    descendants = []
    for child in children:
        d = find_descendants(child, pattern, generation - 1)
        descendants.extend(d)
    return descendants


def rm_files_in(folder: StrPath, ext: str) -> None:
    """删除文件夹内指定扩展名文件"""
    for f in Path(folder).glob('*' + ext):
        Path(f).unlink()


def remake_dir(parent: StrPath, name: str) -> Path:
    """删除并重建目录"""
    path = Path(parent, name)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def make_parents(p: StrPath) -> Path:
    """创建上级目录"""
    p = Path(p).parent
    p.mkdir(parents=True, exist_ok=True)
    return p


def or_ext(file: StrPath, ext: str) -> Path:
    """如果不存在，则补充扩展名"""
    file = Path(file)
    if not file.suffix and ext:
        file = file.with_suffix(ext)
    return file


def last_parts(file: StrPath, n: int) -> Path:
    """获取路径最后的n部分"""
    p = Path(file)
    return Path(*p.parts[-n:])


def with_parent(file: StrPath, parent: str) -> Path:
    """替换上级目录名"""
    file = Path(file)
    return file.parent.parent / parent / file.name


def find_pattern(folder: StrPath, ext: str, pattern: str) -> Generator[Path, Any, None]:
    """查找匹配指定模式的文件"""
    for f in Path(folder).rglob('*' + ext):
        if re.search(pattern, str(f)):
            yield f


def time_to_file(time: Arrow, ext: str, date_dir: bool = True) -> str:
    """时间转为文件名"""
    s = '/' if date_dir else '_'
    fmt = '%Y-%m-%d' + s + '%H-%M-%S.%f'
    name = time.strftime(fmt)[:-3] + ext
    return name


def device_time_file(folder: Path, dev_id: int | str, time: Arrow, ext: str, date_dir: bool = True) -> Path:
    """根据设备ID,所在目录创建时间为名称的文件"""
    file = time_to_file(time, ext, date_dir)
    p = Path(folder, str(dev_id), file)
    make_parents(p)
    return p


def not_file_to_time(path: StrPath) -> Arrow:
    """文件名转时间 2023-04-10_10-09-39.830"""
    p = Path(path)
    s = '%sT%s+%s' % (p.parent.name, p.stem.replace('-', ':'), '08:00')
    return arrow.get(s)


def link_files(src_files: list[Path], dst_dir: Path, check_fun: Optional[Callable[[Path], bool]] = None) -> None:
    """链接文件列表到目标目录"""
    for f in src_files:
        dst = dst_dir / f.name
        dst.parent.mkdir(exist_ok=True, parents=True)
        dst.symlink_to(f.absolute())
        if check_fun and not check_fun(dst):
            logger.error(f'check fail: {dst}')


def real_path(path: StrPath) -> Path:
    """"获取真实文件"""
    p = Path(path)
    return Path(os.readlink(p)) if p.is_symlink() else p


def real_exe_path() -> Path:
    """"获取真实可执行文件路径"""
    return real_path(sys.argv[0])


def copy_file(src: Path, dst: Path) -> Result[Path, IOError]:
    """复制文件"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copyfile(src, dst)
    except IOError as e:
        return Err(e)
    return Ok(dst)


def move_file(src: Path, dst: Path) -> Result[Path, IOError]:
    """移动文件"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(src, dst)
    except IOError as e:
        return Err(e)
    return Ok(dst)


def insert_dir(folder: StrPath, dir_name: str) -> None:
    """在目录中插入一级目录, 原目录内的文件移动如新目录"""
    folder = Path(folder)
    assert folder.is_dir()
    tmp = folder.parent / (folder.name + '_tmp')
    dst = folder / dir_name
    shutil.move(folder, tmp)

    assert not folder.exists()
    folder.mkdir()
    assert folder.exists()
    shutil.move(tmp, dst)


def file_ctime(file: StrPath) -> Arrow:
    """获取文件的建立时间"""
    t = Path(file).stat().st_ctime  # 创建时间
    return Arrow.fromtimestamp(t)


def file_mtime(file: StrPath) -> Arrow:
    """获取文件的修改时间"""
    t = Path(file).stat().st_mtime  # 创建时间
    return Arrow.fromtimestamp(t)


def ctime_to_name(src: Path) -> str:
    """以文件创建时间生成文件名"""
    return time_to_file(file_ctime(src), src.suffix)


def mtime_to_name(src: Path) -> str:
    """以文件修改时间生成文件名"""
    return time_to_file(file_mtime(src), src.suffix)


'''
_file_now: Option[Arrow] = Null  # TODO: 用Iter对象重写

def now_to_name(src: Path) -> str:
    """以当前文件时间生成文件名"""
    global _file_now
    match _file_now:
        case Null:
            _file_now = file_mtime(src)
        case Some(v):
            v = _file_now.shift(seconds=1)
    return time_to_file(_file_now.unwrap(), src.suffix)
'''


def stem_append(p: Path, s: str) -> Path:
    """文件名主干后面追加字符串"""
    return p.parent / (p.stem + s + p.suffix)


def name_with_parents(path: StrPath, num_parents: int) -> Option[str]:
    """路径转换成文件名, 文件名中带有指定数量的上级目录, REMARK: 避免上级目录中包含根目录"""
    parts = list(Path(path).parts)
    start = len(parts) - 1 - num_parents
    if start < 0:
        return Null
    name = '_'.join(parts[start:])
    return Some(name)


def replace_home(p: StrPath) -> Path:
    """替换~为HOME目录"""
    p = str(p).replace('~', str(Path.home()))
    return Path(p)


def remove_parent_prefix(p: StrPath) -> Result[Path, str]:
    """从文件名中去掉所在目录名前缀"""
    p = Path(p)
    if p.name.startswith(p.parent.name):
        p1 = p.parent / p.name[len(p.parent.name) + 1:]
        return Ok(p1)
    return Err('No prefix')


def du(path: StrPath) -> int:
    s = sh.du('-s', path)
    size, _ = parse('{}\t{}', s)
    return int(size)

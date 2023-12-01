#!/usr/bin/env python3

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class FileInfo:
    path: Path
    md5: str


def file_map(folder: Path) -> Dict[int, FileInfo]:
    m: Dict[int, FileInfo] = {}
    for f in folder.rglob('*.*'):
        if f.is_file():
            info = FileInfo(f, calc_md5(f))
            size = f.stat().st_size
            if size not in m:
                m[size] = []
            m[size] = info
    return m


def calc_md5(file: Path) -> str:
    m = hashlib.md5()  # 创建md5对象
    print(f'{file}')
    with open(file, 'rb') as f:
        data = f.read(1 << 20)
        m.update(data)  # 更新md5对象

    return m.hexdigest()  # 返回md5对象


def main() -> None:
    parser = argparse.ArgumentParser('对照源目录, 删除目标目录的重复文件')
    parser.add_argument('src_dir', type=Path, help='文件来源目录')
    parser.add_argument('dst_dir', type=Path, help='文件目标目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    src_map = file_map(opt.src_dir)
    dst_map = file_map(opt.dst_dir)

    for size, dst_info in dst_map.items():
        if size in src_map:
            src_info = src_map.get(size)
            assert src_info
            if src_info.md5 == dst_info.md5:
                print(f'REMOVE: "{dst_info.path}"\n    as: "{src_info.path}"')
                try:
                    dst_info.path.unlink()
                except OSError as e:
                    print(f"ERROR: {dst_info.path} {e}")


if __name__ == '__main__':
    main()

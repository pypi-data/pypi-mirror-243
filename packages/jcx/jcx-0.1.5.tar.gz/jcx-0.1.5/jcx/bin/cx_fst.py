#!/usr/bin/env python3

import argparse
import glob
import os
import sys
from collections import defaultdict
from os.path import splitext

from jcx.sys.fs import StrPath, dirs_in, insert_dir


def main() -> None:
    parser = argparse.ArgumentParser(description='文件系统工具箱')
    parser.add_argument('path', metavar='PATH', type=str, help='目录')
    parser.add_argument('-s', '--same-name-count', type=int, help='重名指定次数的文件，同目录，不计扩展名')
    parser.add_argument('-d', '--include-dir', action='store_true', default=False, help='是否包含目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    if os.path.isdir(opt.path):
        s = os.path.join(opt.path, "**/*")
        files = sorted(glob.glob(s, recursive=True))
    else:
        print("目录不存在：", opt.path)
        sys.exit(0)

    if not opt.include_dir:
        files = [f for f in files if not os.path.isdir(f)]

    counters = defaultdict(int)
    for f in files:
        f0 = splitext(f)[0]
        counters[f0] += 1

    for f in files:
        f0 = splitext(f)[0]
        if counters[f0] == opt.same_name_count:
            print(f)


def insert_channel(folder: StrPath) -> None:
    """给抓图目录插入channel"""

    dirs = dirs_in(folder)
    for i, d in enumerate(dirs):
        print(f'#{i:04}  {d}')
        insert_dir(d, '0')


if __name__ == '__main__':
    main()
    # insert_channel('/var/ias/snapshot/shtm/n1')

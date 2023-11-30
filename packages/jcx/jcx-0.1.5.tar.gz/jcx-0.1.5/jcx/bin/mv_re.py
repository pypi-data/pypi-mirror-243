#!/usr/bin/env python3

import re
import shutil
import sys
from pathlib import Path
from typing import Optional


def re_cap_fmt(src_str: str, pattern: str, dst_fmt: str) -> Optional[str]:
    """"RE捕获 & 替换"""
    m = re.search(pattern, src_str)
    if m is None:
        return None
    for i, g in enumerate(m.groups()):
        dst_fmt = dst_fmt.replace("(%d)" % (i + 1), g)
    dst_fmt = dst_fmt.replace("(0)", m.group(0))
    return dst_fmt


def main():
    if len(sys.argv) != 4:
        print(r"""
    Usage:
        mv-re.py src_path src_re dst_fmt
    samples:
        mv-re.py ./2016-05-06/57 './([^/]+)/(\d+)' '../(2)/(1)'
        find -type d -exec mv-re.py {} "\./([^/]+)/(\d+)" "../(2)/(1)" \;
        find -name '*.mp4' -exec mv-re.py {} "[^_]+_(.+)" "(1)" \;
    """)

        sys.exit(1)

    src_path = sys.argv[1]  # 指明被遍历的文件夹
    src_re = sys.argv[2]  # 源RE
    dst_fmt = sys.argv[3]  # 目标格式

    dst_path = re_cap_fmt(src_path, src_re, dst_fmt)

    if dst_path is not None:
        Path(dst_path).parent.mkdir(exist_ok=True, parents=True)
        print("move '%s' to '%s'" % (src_path, dst_path))
        shutil.move(src_path, dst_path)


if __name__ == '__main__':
    main()

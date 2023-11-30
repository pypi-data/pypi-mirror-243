#!/usr/bin/env python3

import os
import os.path
import re
import sys
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
        rename-re.py dir src_re dst_fmt
    samples:
        rename-re.py . '(\d+)_(\d+).jpg' '(2)_(1).jpg'
        rename-re.py . '(\w+).jpg' '(0)_(1).jpg'
    """)
        sys.exit(1)

    root_dir = sys.argv[1]  # 指明被遍历的文件夹
    pattern = sys.argv[2]  # 源RE
    repl = sys.argv[3]  # 目标格式

    for parent, dir_names, file_names in os.walk(root_dir):
        for file_name in file_names:  # 输出文件信息
            new_name = re_cap_fmt(file_name, pattern, repl)
            if new_name is not None:
                os.rename(os.path.join(parent, file_name), os.path.join(parent, new_name))
                # shutil.move(os.path.join(parent, file_name), os.path.join(parent, new_name))
                print("rename '%s' to '%s'" % (file_name, new_name))


if __name__ == '__main__':
    main()

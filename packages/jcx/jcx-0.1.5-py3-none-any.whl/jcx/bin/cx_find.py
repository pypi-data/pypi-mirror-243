#!/opt/ias/env/bin/python

import argparse
from pathlib import Path

from jcx.sys.fs import files_in


def has_mate(file: Path, names: list) -> bool:
    """检查文件是否有伙伴文件"""
    for name in names:
        # print('math:', name, file.stem)
        if name.startswith(file.stem):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser('文件查找工具')
    parser.add_argument('src_dir', type=Path, help='文件来源目录')
    parser.add_argument('-e', '--ext', type=str, default='jpg', help='文件扩展名')
    parser.add_argument('-m', '--mate_ext', type=str, default='lbl', help='文件伙伴文件扩展名')
    parser.add_argument('-i', '--invert_match', action='store_true', help='选中不匹配的文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    mates = files_in(opt.src_dir, opt.mate_ext)
    names = [f.stem for f in mates]

    candidates = files_in(opt.src_dir, opt.ext)

    for f in candidates:
        if has_mate(f, names) != opt.invert_match:
            print(f)


if __name__ == '__main__':
    main()

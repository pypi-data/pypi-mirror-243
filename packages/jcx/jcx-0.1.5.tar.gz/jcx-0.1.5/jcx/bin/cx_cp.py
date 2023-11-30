#!/usr/bin/env python3

import argparse
import glob
import os
import sys
from shutil import copyfile


def folder_files(folder, ext):
    if os.path.isdir(folder):
        s = os.path.join(folder, '**/*.' + ext)
        files = glob.glob(s, recursive=True)
        files.sort()
    else:
        print("数据源不存在:", folder)
        sys.exit(0)
    return files


def copy_file(src, dst):
    try:
        copyfile(src, dst)
        print(' ', dst)
    except IOError as e:
        print("无法复制文件：%s 错误信息：%s" % (src, e))


def main() -> None:
    parser = argparse.ArgumentParser('文件复制工具')
    parser.add_argument('src_dir', type=str, help='文件来源目录')
    parser.add_argument('dst_dir', type=str, help='文件目标目录')
    parser.add_argument('-e', '--ext', type=str, default='jpg', help='文件扩展名')
    parser.add_argument('-r', '--retain_num', type=int, default=5, help='保留的路径节数')
    parser.add_argument('-m', '--make_date_dir', action='store_true', help='创建日期目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    files = folder_files(opt.src_dir, opt.ext)

    for src in files:
        parts = src.split('/')[-opt.retain_num:]
        name = '_'.join(parts)
        dst = os.path.join(opt.dst_dir, name)
        copy_file(src, dst)


if __name__ == '__main__':
    main()

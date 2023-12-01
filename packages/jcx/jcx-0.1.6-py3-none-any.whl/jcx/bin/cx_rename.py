import argparse
import shutil
from pathlib import Path

from jcx.sys.fs import files_in, mtime_to_name, ctime_to_name


def main():
    parser = argparse.ArgumentParser('文件改名/复制工具')
    parser.add_argument('src_dir', type=Path, help='文件来源目录')
    parser.add_argument('dst_dir', type=Path, help='文件目标目录')
    parser.add_argument('-e', '--ext', type=str, default='jpg', help='文件扩展名')
    parser.add_argument('-m', '--method', type=str, required=True,
                        help='改名方法：ctime-改为创建时间, mtime-改为修改时间, now-改为当前时间')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    methods = {'ctime': ctime_to_name, 'mtime': mtime_to_name}
    method = methods[opt.method]

    files = files_in(opt.src_dir, opt.ext)
    for src in files:
        name = method(src)
        dst = Path(opt.dst_dir) / name
        print(src.name, ' -> ', dst.name)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)


if __name__ == '__main__':
    main()

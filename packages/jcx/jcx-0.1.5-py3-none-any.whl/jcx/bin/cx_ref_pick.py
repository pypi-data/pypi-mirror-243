import argparse
import shutil
from pathlib import Path

from jcx.sys.fs import files_in


def main() -> None:
    parser = argparse.ArgumentParser('从参考目录选择文件名, 从候选目录选出文件')
    parser.add_argument('ref_dir', type=Path, help='参考文件目录')
    parser.add_argument('candi_dir', type=Path, help='候选文件目录')
    parser.add_argument('dst_dir', type=Path, help='候选文件目录')
    parser.add_argument('-r', '--ref_ext', type=str, default='json', help='参考文件扩展名')
    parser.add_argument('-o', '--candi_ext', type=str, default='jpg', help='候选文件扩展名')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    assert Path(opt.ref_dir).is_dir(), '参考文件目录不存在: ' + opt.ref_dir
    assert Path(opt.candi_dir).is_dir(), '候选文件目录不存在: ' + opt.candi_dir

    mates = files_in(opt.ref_dir, opt.ref_ext)
    names = [f.stem for f in mates]

    for i, name in enumerate(names):
        f = Path(opt.candi_dir, name + '.' + opt.candi_ext)
        assert Path(f).is_file(), f'文件不存在: {f}'
        shutil.copy(f, opt.dst_dir)


if __name__ == '__main__':
    main()

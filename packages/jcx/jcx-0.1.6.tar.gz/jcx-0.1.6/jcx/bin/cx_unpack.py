import argparse
import subprocess
from pathlib import Path

from jcx.sys.fs import du
from loguru import logger

cmd_map = {
    '.zip': ['unzip' '-O' 'GBK']
}


def main():
    parser = argparse.ArgumentParser('解压缩工具')
    parser.add_argument('file', type=Path, help='待解压文件')
    parser.add_argument('--remove', action='store_true', help='转化成功则删除源文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    src_file = Path(opt.file)
    cmd = cmd_map.get(src_file.suffix)
    if cmd is None:
        return logger.error(f'未知文件格式: {src_file}')

    src_size = src_file.stat().st_size
    if src_size < 1000:
        return logger.error(f'源文件尺寸无效: {src_file}({src_size})')

    dst_file = src_file.with_suffix('')
    if not dst_file.exists():
        cmd.append(str(src_file))
        r = subprocess.call(cmd)
        if r != 0:
            return logger.error(f'解压失败, r={r}, file={dst_file}')

    if not dst_file.exists():
        return logger.error(f'目标路径不存在: {dst_file}')

    dst_size = du(dst_file)

    radio = int(dst_size / src_size * 100)
    logger.debug(f'{src_file}({radio}%)')

    if radio < 100:
        return logger.error(f'解压文件尺寸小于源文件: {src_file}')

    if opt.remove:
        src_file.unlink()
        logger.info('源文件删除!')


if __name__ == '__main__':
    main()

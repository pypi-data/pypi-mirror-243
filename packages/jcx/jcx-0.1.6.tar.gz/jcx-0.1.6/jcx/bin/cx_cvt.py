#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

from loguru import logger


def main():
    parser = argparse.ArgumentParser('图像转换工具')
    parser.add_argument('file', type=Path, help='待转换文件')
    parser.add_argument('ext', type=str, help='目标文件扩展名, 如: .jpg')
    parser.add_argument('--remove', action='store_true', help='转化成功则删除源文件')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    src_file: Path = opt.file  # type: ignore
    if src_file.suffix == opt.ext:
        return

    src_size = src_file.stat().st_size
    if src_size < 1000:
        logger.error(f'源文件尺寸无效: {src_size}')
        return

    dst_file: Path = src_file.with_suffix(opt.ext)  # type: ignore
    if not dst_file.exists():
        r = subprocess.call(['convert', src_file, dst_file])
        if r != 0:
            logger.error(f'转换失败, r={r}, file={dst_file}')
            return
    if not dst_file.exists():
        logger.error(f'目标路径不存在: {dst_file}')
        return

    r = subprocess.call(['identify', dst_file])
    if r != 0:
        logger.error(f'验证失败: {r}')
        return

    dst_size = dst_file.stat().st_size
    if dst_size < 1000:
        logger.error(f'目标文件尺寸无效: {dst_size}')
        return

    radio = int(dst_size / src_size * 100)
    logger.debug(f'{src_file}({radio}%)')

    if opt.remove:
        src_file.unlink()
        logger.info(f'{src_file} 删除!')


if __name__ == '__main__':
    main()

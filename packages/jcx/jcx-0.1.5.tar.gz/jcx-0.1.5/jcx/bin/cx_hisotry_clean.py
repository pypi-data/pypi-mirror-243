
import argparse
from pathlib import Path

from jcx.sys.fs import move_file, replace_home
from jcx.text.io import save_lines
from jcx.time.dt import now_file


def main():
    parser = argparse.ArgumentParser('History文件清理工具')
    parser.add_argument('-f', '--history-file', type=Path, default='~/.zsh_history', help='History文件')
    parser.add_argument('-b', '--backup-dir', type=Path, default='~/.config/history_arch', help='History文件备份目录')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')
    opt = parser.parse_args()

    history_file = replace_home(opt.history_file)
    backup_dir = replace_home(opt.backup_dir)

    cmd_counts = {}
    lines = []
    num_lines = 0
    for i, line in enumerate(open(history_file)):
        num_lines += 1
        r = line.split(';', 1)
        if len(r) != 2:
            print('WARN @ %d: ' % i, line)
            continue
        _, cmd = r
        if cmd not in cmd_counts:
            lines.append(line)
            cmd_counts[cmd] = 0
        cmd_counts[cmd] += 1

    for k, v in cmd_counts.items():
        if v > 1:
            print('n=', v, k)

    bak_file = backup_dir / now_file()
    print('备份历史文件到：', bak_file)
    move_file(history_file, bak_file).unwrap()

    print('历史文件，行数变化：%d -> %d' % (num_lines, len(lines)))
    save_lines(lines, history_file)


if __name__ == '__main__':
    main()

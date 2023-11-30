from typing import Optional

from jcx.sys.fs import or_ext, StrPath
from rustshed import Result, Ok, Option, Some, Err


def load_txt(file: StrPath) -> Result[str, str]:
    """加载文本"""
    with open(file, 'r') as f:
        s = f.read()
        return Ok(s)
    # return Err('load_txt fail.')


def save_txt(txt: str, file: StrPath, ext: str = '.txt') -> Result[bool, Exception]:
    """保存文本到文件"""
    file = or_ext(file, ext)
    try:
        file.parent.mkdir(parents=True, exist_ok=True)
        with open(file, 'w') as f:
            f.write(txt)
    except Exception as e:
        return Err(e)
    return Ok(True)


def save_lines(lines: list[str], file: StrPath, ext: str = '', postfix: str = '') -> None:
    """多行文本保存到文件，文件自动加扩展名，自动建立目录，行尾自动加回车"""
    file = or_ext(file, ext)
    file.parent.mkdir(parents=True, exist_ok=True)
    print('save:', file)
    with open(file, 'w') as f:
        for line in lines:
            f.write(line + postfix)


def replace_in_file(src_file: StrPath, input_: str, output: str, dst_file: Optional[StrPath] = None) -> None:
    """文本文件替换"""
    dst_file = dst_file or src_file

    txt = load_txt(src_file).unwrap()
    new_data = txt.replace(input_, output)
    save_txt(new_data, dst_file)

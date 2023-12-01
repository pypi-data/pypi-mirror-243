from typing import Any
from typing import TypeVar, Type

from pydantic import BaseModel, TypeAdapter
from rustshed import Result, Ok, Err, result_shortcut

from jcx.sys.fs import or_ext, StrPath
from jcx.text.io import save_txt

BMT = TypeVar('BMT', bound=BaseModel)
"""BaseModel派生类型"""


def load_txt(file: StrPath, ext: str = '.txt') -> Result[str, Exception]:
    """从文件加载文本"""
    file = or_ext(file, ext)
    try:
        with open(file, 'r', encoding='utf-8') as f:
            txt = f.read()
    except Exception as e:
        return Err(e)
    return Ok(txt)


def to_json(ob: BMT, pretty: bool = True) -> str:
    """对象序列化为JSON"""
    indent = 4 if pretty else None
    return ob.model_dump_json(indent=indent)


def from_json(json: str | bytes, ob_type: Type[BMT]) -> Result[BMT, Exception]:
    """从JSON文本构建对象"""
    assert isinstance(json, str | bytes), 'Invalid input type @ try_from_json'
    try:
        ob = TypeAdapter(ob_type).validate_json(json)
    except Exception as e:
        return Err(e)
    return Ok(ob)


def save_json(obj: Any, file: StrPath, pretty: bool = True) -> Result[bool, Exception]:
    """对象序保存为JSON文件"""
    file = or_ext(file, '.json')
    s = to_json(obj, pretty)
    return save_txt(s, file)


@result_shortcut
def load_json(file: StrPath, obj_type: Type[BMT]) -> Result[BMT, Exception]:
    """从Json文件加载对象"""
    file = or_ext(file, '.json')
    s = load_txt(file).Q
    # print('load_json:', file)
    return from_json(s, obj_type)

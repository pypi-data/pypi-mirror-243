import traceback
from typing import Callable, TypeVar, Optional, Any

from loguru import logger
from rustshed import Err

T = TypeVar('T')


def mand(value: Optional[T]) -> T:
    """强制可选类型非空"""
    assert value is not None
    return value


def show_err(e: Any) -> None:
    """显示错误/异常"""
    if isinstance(e, Err):
        msg = f'{e}'
    # elif isinstance(e, UnwrapError):
    #    msg = 'UnwrapError(%s):' % str(e.result.value)
    elif isinstance(e, AssertionError):
        msg = f'AssertionError({e.args})'
    else:
        msg = f'UnknownError({repr(e)})'
    logger.error(msg)


def catch_show_err(fun: Callable, verbose: bool = False) -> None:
    """捕获并显示异常"""

    # 捕获SystemExit/KeyboardInterrupt/GeneratorExit外异常
    # 想捕获这三个异常，需BaseException
    try:
        fun()
    except Exception as e:
        show_err(e)
        # print('traceback.print_exc():', traceback.print_exc())
        if verbose:
            print(traceback.format_exc())


def show_err_demo() -> None:
    e = Err('a error')
    print(type(e))
    show_err(e)


if __name__ == '__main__':
    show_err_demo()

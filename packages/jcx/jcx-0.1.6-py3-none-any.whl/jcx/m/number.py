import hashlib
from fractions import Fraction
from typing import TypeAlias, Any

from jcx.text.txt_json import to_json

# 实数类型
Real: TypeAlias = int | float

# 2维实数类型
Real2D: TypeAlias = tuple[Real, Real]

# 2维实数类型
Real1_2D: TypeAlias = Real | Real2D


def is_real(n: Any) -> bool:
    """判断变量是否为实数"""
    return isinstance(n, int) or isinstance(n, float)


def real_2d(n: Real1_2D) -> Real2D:
    """Real1_2D转为2D实数"""

    if isinstance(n, tuple):
        assert len(n) == 2
        x, y = n
    else:
        x, y = n, n
    assert is_real(x) and is_real(y)
    return x, y


def align_down(a: int, b: int) -> int:
    """"整数向下对齐到第二个整数倍数"""
    return int(a / b) * b


def align_up(a: int, b: int) -> int:
    """"整数向上对齐到第二个整数倍数"""
    return align_down(a + b - 1, b)


def is_multiple(a: int, b: int) -> int:
    """判定a是否是b的整数倍"""
    return a % b == 0


def align_round(n: float, align_num: int) -> int:
    """近似对齐"""
    return int(n + align_num / 2) // align_num * align_num


def a_fraction() -> None:
    f1 = Fraction(16, -10)
    print(f1)
    s = to_json(f1)
    print(s)


def md5_int(src: str, mod: int) -> int:
    """md5哈希算法返回整数"""
    md5 = hashlib.md5()
    md5.update(src.encode('utf-8'))
    n = 1
    s = 0
    for d in md5.digest():
        s = s + d * n
        n = n * 256 % mod
    return s % mod

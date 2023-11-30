import numpy as np
from jcx.util.algo import lookup


def random_split_n(n: int, radios: list) -> list[list]:
    """按比例随机分割整数集合[0,n-1]"""

    radios_np = np.array(radios)
    s = 0
    for i in range(len(radios_np)):
        s += radios_np[i]
        radios_np[i] = s
    radios_np = radios_np / s

    ends = (radios_np * n).astype(int)

    array = np.arange(n)
    np.random.shuffle(array)

    start = 0
    slices: list[list] = []
    for end in ends:
        slice: list = array[start:end].tolist()
        slices.append(slice)
        start = end
    return slices


def random_split_array(arr: list, radio_arr: list) -> list:
    """按比例随机分割数组"""

    slices = random_split_n(len(arr), radio_arr)
    return [lookup(s, arr) for s in slices]


def random_split(x: int | list, radio: list) -> list:
    """按比例随机分割整数集合或数组"""

    if isinstance(x, int):
        return random_split_n(x, radio)
    if isinstance(x, list):
        return random_split_array(x, radio)
    raise 'Unknown type'


def random_split_test() -> None:
    slices = random_split(10, [8, 1, 1])
    for s in slices:
        print(s)

    arr = [chr(ord('a') + i) for i in range(10)]
    print(arr)

    slices = random_split(arr, [8, 1, 1])
    for s in slices:
        print(s)


def group(arr: list, group_member: int) -> list[list]:
    """分组"""

    total = len(arr)
    return [arr[i: i + group_member] for i in range(0, total, group_member)]


def group_test() -> None:
    a = [i for i in range(11)]
    print(a)
    print(group(a, 5))


if __name__ == '__main__':
    # list_index_test()
    # random_split_test()
    group_test()

import math


def sqrt1(n):
    a = int(math.sqrt(n))
    b = n - a * a
    r = a + b / (2 * a)
    return r


def sqrt2(n):
    a = int(math.sqrt(n))
    b = n - a * a
    r = a + b / (2 * a) - b * b / (8 * a * a * a)
    return r


def a_num(n) -> None:
    r = math.sqrt(n)
    r1 = sqrt1(n)
    r2 = sqrt2(n)
    print('%d:\t%0.6f\t%0.10f\t%0.10f' % (n, r, r1 - r, r2 - r))


def a_test() -> None:
    a_num(85)

    a_num(101)
    a_num(10001)
    a_num(10101)
    a_num(10181)
    a_num(686756)
    a_num(909090909090909999)


if __name__ == '__main__':
    a_test()

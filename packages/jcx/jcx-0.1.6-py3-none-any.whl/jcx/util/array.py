class Array(list[int]):
    """可以继承自 List"""

    def __init__(self, arr):
        super().__init__()
        self.extend(arr)

    def hi(self):
        print('hi array')


def test_array():
    arr = [1, 2, 4, 8, 16]

    a = Array(arr)
    a.extend(arr)
    print(a)
    a.hi()

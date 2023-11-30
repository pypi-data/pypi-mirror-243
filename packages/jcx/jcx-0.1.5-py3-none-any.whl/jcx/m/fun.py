from dataclasses import dataclass


@dataclass
class Linear:
    """线性函数"""
    k: float
    b: float

    @classmethod
    def from_xyxy(cls, x1: float, y1: float, x2: float, y2: float) -> 'Linear':
        """构造, 用: x1, y1, x2, y2"""
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return Linear(k, b)

    def __call__(self, x: float) -> float:
        y = self.k * x + self.b
        return y

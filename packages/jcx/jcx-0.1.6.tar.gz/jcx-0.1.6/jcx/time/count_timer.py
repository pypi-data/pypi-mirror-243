from dataclasses import dataclass


@dataclass
class Counter:
    """计数器"""
    count: int = 0
    """计数值"""

    def __str__(self):
        return 'Counter(%d)' % self.count

    def get(self) -> int:
        """获取计数值"""
        return self.count

    def get_inc(self) -> int:
        """获取计数值并更新计数器"""
        t = self.get()
        self.count += 1
        return t


@dataclass
class CountTimer:
    """计数闹钟"""
    interval: int
    """间隔"""
    count: int = 0
    """计数值"""

    def __str__(self):
        return 'CountTimer(%d,%d)' % (self.interval, self.count)

    def inc(self):
        """更新计数器"""
        self.count += 1

    def check(self) -> bool:
        """计数器是否到规定的间隔"""
        return self.count >= self.interval

    def inc_check(self) -> bool:
        """计数器累计，并检查是否到规定的间隔"""
        self.inc()
        return self.check()

    def auto_check(self) -> bool:
        """计数器累计，并检查是否到规定的间隔，到规定时间则自动复位"""
        ok = self.inc_check()
        if ok:
            self.reset()
        return ok

    def reset(self):
        """计数器复位"""
        self.count = 0

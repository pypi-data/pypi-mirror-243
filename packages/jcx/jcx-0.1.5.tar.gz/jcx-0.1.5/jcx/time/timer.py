from datetime import timedelta

from arrow import Arrow


class Timer:
    """更新时间记录"""

    def __init__(self, last_updated=Arrow(1970, 1, 1)):
        self.__last_updated = last_updated  # 上一次更新时间

    def __str__(self):
        return 'Timer(%s)' % str(self.__last_updated)

    def next(self, interval: timedelta) -> Arrow:
        """预计下次更新时间"""
        return self.__last_updated + interval

    def check(self, time: Arrow, interval: timedelta) -> bool:
        """检查时间是否到达更新时间"""
        n = self.next(interval)
        return time >= n

    def update(self, time: Arrow):
        """更新时间"""
        self.__last_updated = time

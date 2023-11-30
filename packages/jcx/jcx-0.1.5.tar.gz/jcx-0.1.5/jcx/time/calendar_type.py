from dataclasses import dataclass, field
from typing import TypeAlias

from jcx.time.clock_time import ClockTime
from rustshed import Result, Ok, Err


@dataclass(frozen=True)
class ClockPeriod:
    """时钟时间段"""
    begin: ClockTime = ClockTime()
    """起始时间"""
    end: ClockTime = ClockTime()
    """截至时间"""

    def __str__(self) -> str:
        return '[%s,%s)' % (self.begin, self.end)

    def __contains__(self, clock_time: ClockTime) -> bool:
        return self.begin <= clock_time < self.end


ClockPeriods: TypeAlias = list[ClockPeriod]
"""时钟时间段集合"""


@dataclass(frozen=True)
class CalendarTrigger:
    """日程表触发器"""

    periods: ClockPeriods = field(default_factory=list)
    """触发时段集合"""

    def start_time(self) -> ClockTime:
        """日程的开始时间"""
        return self.periods[0].begin if self.periods else ClockTime()

    def check(self, clock_time: ClockTime) -> bool:
        """判定时间是否满足日历触发条件"""
        # 时段检查
        ok = False
        if self.periods:
            for p in self.periods:
                if clock_time in p:
                    ok = True
                    break
        else:
            ok = True
        # 检查星期 TODO:
        return ok

    def valid(self) -> Result[bool, str]:
        """判断是否有效"""
        if len(self.periods) > 0:
            return Ok(True)
        return Err('日程表触发器时段不存在')


CalendarTriggers: TypeAlias = list[CalendarTrigger]  # 时钟时间段集合

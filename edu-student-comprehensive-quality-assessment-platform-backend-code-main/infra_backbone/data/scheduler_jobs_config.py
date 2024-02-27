"""
排程任务配置文件
"""
from datetime import date, datetime
from typing import Dict, Optional, Union

from flask import Flask


class SchedulerJobsConfig:
    """
    排程任务配置文件
    """

    def __init__(self, setup_option: Dict):
        """
        初始化
        Args:
            setup_option:
        """
        self.id: str = setup_option.get("id", None)
        self.func_name: str = setup_option.get("func_name", None)
        self.func_args: str = setup_option.get("func_args", None)
        self.trigger_category: str = setup_option.get("trigger_category", None)
        self.start_date: Optional[Union[date, datetime, str]] = setup_option.get("start_date", None)
        self.end_date: Optional[Union[date, datetime, str]] = setup_option.get("end_date", None)
        self.app: Flask = setup_option.get("app", None)

    def dict(self):
        """
        把类的属性转换为字典
        Returns:

        """
        return self.__dict__


class SchedulerJobsConfigForInterval(SchedulerJobsConfig):
    """
    排程任务配置文件 以固定的时间间隔运行
    """

    def __init__(self, setup_option: Dict):
        """
        初始化
        Args:
            setup_option:
        """
        super().__init__(setup_option)
        self.weeks: Optional[int] = setup_option.get("weeks", None)
        self.days: Optional[int] = setup_option.get("days", None)
        self.hours: Optional[int] = setup_option.get("hours", None)
        self.minutes: Optional[int] = setup_option.get("minutes", None)
        self.seconds: Optional[int] = setup_option.get("seconds", None)


class SchedulerJobsConfigForCron(SchedulerJobsConfig):
    """
    排程任务配置文件 在特定时间定期运行
    """

    def __init__(self, setup_option: Dict):
        """
        初始化
        Args:
            setup_option:
        """
        super().__init__(setup_option)
        self.year: Union[str, int] = setup_option.get("year", None)
        self.month: Union[str, int] = setup_option.get("month", None)
        self.day: Union[str, int] = setup_option.get("day", None)
        self.week: Union[str, int] = setup_option.get("week", None)
        self.day_of_week: Union[str, int] = setup_option.get("day_of_week", None)
        self.hour: Union[str, int] = setup_option.get("hour", None)
        self.minute: Union[str, int] = setup_option.get("minute", None)
        self.second: Union[str, int] = setup_option.get("second", None)

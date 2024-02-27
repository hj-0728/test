from datetime import datetime, timedelta
from enum import Enum

from infra_basic.basic_model import BasePlusModel
from pydantic import root_validator


class EnumPeriodCategoryDate(Enum):
    """
    周期类型 code
    """

    DAY = "今天"
    WEEK = "本周"
    MONTH = "本月"
    SEMESTER = "本学期"


class PeriodCategoryDateViewModel(BasePlusModel):
    """
    周期分类日期
    """

    name: str
    value: str
    started_on: datetime
    ended_on: datetime

    @root_validator
    def validate_period_category(cls, values):
        """
        验证周期类型
        :param values:
        :return:
        """
        values["started_on"] = values["started_on"].replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        values["ended_on"] = values["ended_on"].replace(hour=0, minute=0, second=0, microsecond=0)
        return values

    @classmethod
    def get_day_dates(cls):
        """
        获取日周期
        :return:
        """
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=1)
        return cls(
            name=EnumPeriodCategoryDate.DAY.value,
            value=EnumPeriodCategoryDate.DAY.name,
            started_on=start_date,
            ended_on=end_date,
        )

    @classmethod
    def get_week_dates(cls):
        """
        获取本周周期
        :return:
        """
        now = datetime.now()
        start_date = now - timedelta(days=now.weekday())
        end_date = start_date + timedelta(days=7)
        return cls(
            name=EnumPeriodCategoryDate.WEEK.value,
            value=EnumPeriodCategoryDate.WEEK.name,
            started_on=start_date,
            ended_on=end_date,
        )

    @classmethod
    def get_month_dates(cls):
        """
        获取本月周期
        :return:
        """
        now = datetime.now()
        start_date = now.replace(day=1)
        if now.month == 12:
            end_date = now.replace(year=now.year + 1, month=1, day=1)
        else:
            end_date = now.replace(month=now.month + 1, day=1)
        return cls(
            name=EnumPeriodCategoryDate.MONTH.value,
            value=EnumPeriodCategoryDate.MONTH.name,
            started_on=start_date,
            ended_on=end_date,
        )

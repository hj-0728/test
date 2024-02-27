from datetime import timedelta
from typing import List

from infra_basic.errors import BusinessError

from biz_comprehensive.model.period_category_model import EnumPeriodCategoryCode
from biz_comprehensive.model.period_model import PeriodModel
from biz_comprehensive.model.view.period_category_date_vm import (
    EnumPeriodCategoryDate,
    PeriodCategoryDateViewModel,
)
from biz_comprehensive.repository.period_repository import PeriodRepository


class PeriodService:
    def __init__(self, period_repository: PeriodRepository):
        self.__period_repository = period_repository

    def get_current_semester_period_info(self) -> PeriodModel:
        """
        获取当前学期周期信息
        :return:
        """
        period = self.__period_repository.get_current_period_info_by_period_category(
            period_category=EnumPeriodCategoryCode.SEMESTER.name
        )
        if not period:
            raise BusinessError("未获取到当前学期")
        return period

    def get_period_category_date(
        self, mini_period_category: str
    ) -> List[PeriodCategoryDateViewModel]:
        """
        获取周期分类日期
        :return:
        """
        result = [
            PeriodCategoryDateViewModel.get_week_dates(),
            PeriodCategoryDateViewModel.get_month_dates(),
        ]
        if mini_period_category == EnumPeriodCategoryDate.DAY.name:
            # 目前只区分捞不捞日回去，如果有其他情况再做相应调整
            result.insert(
                0,
                PeriodCategoryDateViewModel.get_day_dates(),
            )
        period = self.get_current_semester_period_info()
        result.append(
            PeriodCategoryDateViewModel(
                name=EnumPeriodCategoryDate.SEMESTER.value,
                value=EnumPeriodCategoryDate.SEMESTER.name,
                started_on=period.started_on,
                ended_on=period.ended_on,
            )
        )
        return result

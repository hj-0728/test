from datetime import datetime
from typing import List, Union

from infra_basic.basic_model import BasePlusModel


class ObservationPointsViewModel(BasePlusModel):
    """
    观察积分
    """

    observation_on: datetime
    class_avg_points: float
    student_total_points: int


class StackedLineDataViewModel(BasePlusModel):
    """
    折线图数据
    """

    name: str
    data: List[Union[int, float]]


class StudentGrowthTrendViewModel(BasePlusModel):
    """
    学生成长趋势雷达图
    """

    observation_date_list: List[datetime]
    data_list: List[StackedLineDataViewModel]

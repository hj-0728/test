from typing import List, Optional, Union

from infra_basic.basic_model import BasePlusModel


class StudentScenePointsViewModel(BasePlusModel):
    """
    学生场景得分
    """

    scene_id: str
    scene_name: str
    class_avg_points: float
    student_total_points: int


class RadarIndicatorViewModel(BasePlusModel):
    """
    雷达图指标
    """

    name: str
    max: Optional[int]


class RadarDataViewModel(BasePlusModel):
    """
    雷达图数据
    """

    name: str
    value: List[Union[int, float]]


class StudentComprehensiveRadarViewModel(BasePlusModel):
    """
    学生综合雷达图
    """

    indicator_list: List[RadarIndicatorViewModel]
    data_list: List[RadarDataViewModel]

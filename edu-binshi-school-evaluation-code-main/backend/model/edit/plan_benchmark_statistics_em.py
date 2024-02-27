"""
command
"""
from enum import Enum
from typing import List, Optional
from infra_basic.basic_model import BasePlusModel


class EnumStatisticsObjectType(str, Enum):
    CLASS = "班级"
    STUDENT = "学生"
    RANKING = "排行"


class EnumObjectIdType(str, Enum):
    GRADE = "年级"
    CLASS = "班级"
    STUDENT = "学生"


class PlanBenchmarkStatisticsEm(BasePlusModel):
    """
    评价计划指标统计
    """

    benchmark_id: str
    evaluation_criteria_plan_id: str
    statistics_object_type: str  # 统计对象类型: 1-班级, 2-学生
    dimension_dept_tree_id_list: Optional[List[str]]  # 若没有则捞全部


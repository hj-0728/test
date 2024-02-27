from enum import Enum

from infra_basic.basic_model import BasePlusModel


class EnumSortMethods(str, Enum):
    INITIALS_NAME = "按姓名首字母排序"
    POINTS = "按积分总分排序"


class LoadClassStudentEditModel(BasePlusModel):
    tree_id: str
    sort_methods: str
    period_id: str

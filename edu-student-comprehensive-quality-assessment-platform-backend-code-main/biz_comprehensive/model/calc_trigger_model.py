from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumCalcTriggerInputResCategory(Enum):
    """
    菜单的category
    """

    OBSERVATION_POINT = "观测点"
    INDICATOR = "指标"


class CalcTriggerModel(VersionedModel):
    """
    计算触发器
    """

    calc_rule_id: str
    input_res_category: str
    input_res_id: str

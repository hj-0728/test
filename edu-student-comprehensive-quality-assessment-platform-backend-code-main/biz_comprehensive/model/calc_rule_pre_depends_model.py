from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumCalcRulePreDependsDependResCategory(Enum):
    """
    计算规则前置依赖资源category
    """

    INDICATOR = "指标"


class CalcRulePreDependsModel(VersionedModel):
    """
    计算规则前置依赖
    """

    calc_rule_id: str
    depend_res_category: str
    depend_res_id: str
    weight: int

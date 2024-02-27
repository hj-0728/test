from enum import Enum
from typing import Any, Dict, Optional

from infra_basic.basic_model import VersionedModel


class EnumBelongsToResCategory(Enum):
    """
    菜单的category
    """

    INDICATOR = "指标"
    SYMBOL = "符号"
    MEDAL = "勋章"
    EVALUATION_CRITERIA = "评价准则"


class EnumCalcFunc(Enum):
    ASSIGN = "assign"
    SUM = "sum"
    WEIGHTING = "weighting"
    RANGE_ASSIGN = "range_assign"


class EnumPreCalcFunc(Enum):
    HANDLE_CALC_RES = "handle_calc_res"


class CalcRuleModel(VersionedModel):
    """
    计算规则
    """

    belongs_to_res_category: str
    belongs_to_res_id: str
    pre_func: Optional[str]
    pre_func_params: Optional[Dict[str, Any]]
    calc_func: Optional[str]
    calc_func_params: Optional[Dict[str, Any]]
    post_func: Optional[str]
    post_func_params: Optional[Dict[str, Any]]

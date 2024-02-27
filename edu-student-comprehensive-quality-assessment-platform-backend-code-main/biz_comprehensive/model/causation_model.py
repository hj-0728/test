from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumCausationEffectResCategory(Enum):
    CALC_LOG = "计算日志"
    MEDAL_ISSUE_LOG = "勋章颁发日志"
    INDICATOR_SCORE_LOG = "指标得分日志"
    POINTS_LOG = "积分日志"


class EnumCausationCauseResCategory(Enum):
    OBSERVATION_POINT_LOG = "观测点日志"
    CALC_COMMAND_LOG = "计算指令日志"


class CausationModel(VersionedModel):
    """
    因果
    """

    cause_res_category: str
    cause_res_id: str
    effect_res_category: Optional[str]
    effect_res_id: Optional[str]
    effected_on: Optional[datetime]

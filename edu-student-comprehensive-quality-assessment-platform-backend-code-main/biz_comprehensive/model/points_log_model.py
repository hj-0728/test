from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumPointsLogStatus(str, Enum):
    """
    积分日志状态
    """

    REVOKED = "已撤回"
    CONFIRMED = "已确定"
    REVERSED = "反冲"


class EnumPointsLogOwnerResCategory(str, Enum):
    """
    积分日志所属资源类型
    """

    ESTABLISHMENT_ASSIGN = "ESTABLISHMENT_ASSIGN"


class PointsLogModel(VersionedModel):
    owner_res_category: str
    owner_res_id: str
    gained_points: float
    symbol_id: str
    balanced_addition: float
    balanced_subtraction: float
    status: str
    expired_on: Optional[datetime]
    belongs_to_period_id: str

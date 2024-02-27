from datetime import datetime
from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumMedalIssuedLogIssuedResCategory(Enum):
    """
    勋章颁发对象的category
    """

    DIMENSION_DEPT_TREE = "dimension_dept_tree"
    ESTABLISHMENT_ASSIGN = "establishment_assign"


class EnumMedalIssuedLogStatus(Enum):
    """
    勋章颁发日志状态
    """

    ISSUED = "颁发"
    REVOKED = "已撤销"


class MedalIssuedLogModel(VersionedModel):
    """
    勋章颁发日志
    """

    medal_id: str
    calc_rule_id: str
    issued_res_category: str
    issued_res_id: str
    issued_on: datetime
    status: str

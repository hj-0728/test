from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumIndicatorScoreLogOwnerResCategory(Enum):
    """
    指标分数日志对象的category
    """

    DIMENSION_DEPT_TREE = "dimension_dept_tree"
    ESTABLISHMENT_ASSIGN = "establishment_assign"


class IndicatorScoreLogModel(VersionedModel):
    """
    指标得分日志
    """

    indicator_score_id: str
    owner_res_category: str
    owner_res_id: str
    string_score: Optional[str]
    numeric_score: Optional[float]

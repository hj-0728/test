from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumIndicatorScoreLogOwnerResCategory(Enum):
    """
    指标最终得分对象的category
    """

    DIMENSION_DEPT_TREE = "dimension_dept_tree"
    ESTABLISHMENT_ASSIGN = "establishment_assign"


class IndicatorFinalScoreModel(VersionedModel):
    """
    指标最终得分
    """

    owner_res_category: str
    owner_res_id: str
    indicator_id: str
    string_score: Optional[str]
    numeric_score: Optional[float]

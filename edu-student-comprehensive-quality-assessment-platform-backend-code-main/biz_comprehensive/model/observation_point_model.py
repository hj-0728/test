from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumObservationPointCategory(Enum):
    """
    观测点的category
    """

    COMMEND = "表扬"
    TO_BE_IMPROVED = "待改进"


class ObservationPointModel(VersionedModel):
    """
    观测点
    """

    name: str
    code: Optional[str]
    category: str

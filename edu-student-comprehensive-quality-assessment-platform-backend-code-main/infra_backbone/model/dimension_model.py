from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDimensionCategory(str, Enum):
    ADMINISTRATION = "行政维度"
    EDU = "教育维度"


class EnumDimensionCode(str, Enum):
    INNER = "内部"
    K12 = "K12"


class DimensionModel(VersionedModel):
    name: str
    code: str
    category: str
    organization_id: Optional[str]

from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDimensionCategory(str, Enum):
    ADMINISTRATION = "行政维度"
    EDU = "教育维度"


class DimensionModel(VersionedModel):
    name: str
    code: str
    category: str
    organization_id: Optional[str]

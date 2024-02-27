from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumOrganizationCategory(str, Enum):
    SCHOOL = "学校"


class OrganizationModel(VersionedModel):
    name: str
    code: Optional[str]
    category_name: Optional[str]
    category: str
    is_activated: bool = True

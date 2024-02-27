from enum import Enum

from infra_basic.basic_model import VersionedModel


class IdentityNumberModel(VersionedModel):
    """
    身份编号
    """

    owner_id: str
    owner_category: str
    category: str
    number: str


class EnumIdentityNumberCategory(Enum):
    """
    身份编号类型
    """

    ID_CARD = "身份证"
    PASSPORT = "护照"


class EnumIdentityNumberOwnerCategory(Enum):
    """
    身份编号所属类型
    """

    PEOPLE = "人员"

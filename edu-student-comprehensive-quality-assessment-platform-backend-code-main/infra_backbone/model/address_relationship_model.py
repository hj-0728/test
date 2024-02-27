from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumAddressRelationshipRelationship(Enum):
    """
    性别
    """

    CURRENT_ADDRESS = "现居住地"
    RESIDENCE_ADDRESS = "户籍地址"


class EnumAddressRelationshipResourceCategory(Enum):
    """
    性别
    """

    PEOPLE = "人员"


class AddressRelationshipModel(VersionedModel):
    address_id: str
    resource_id: str
    resource_category: str
    relationship: Optional[str]

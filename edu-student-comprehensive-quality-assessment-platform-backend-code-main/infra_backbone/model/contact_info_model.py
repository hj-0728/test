from enum import Enum
from typing import Optional

from infra_basic.basic_model import BasicModel
from pydantic.main import BaseModel


class ContactInfoModel(BasicModel):
    resource_contact_info_id: Optional[str]
    category: str
    detail: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ContactInfoModel):
            return NotImplemented
        return self.category == other.category and self.detail == other.detail


class EnumContactInfoCategory(Enum):
    SHORT_PHONE_NUMBER = "短号"
    PHONE = "手机号"
    LANDLINES = "座机号"


class ContactInfoCategory(BaseModel):
    name: str
    value: str

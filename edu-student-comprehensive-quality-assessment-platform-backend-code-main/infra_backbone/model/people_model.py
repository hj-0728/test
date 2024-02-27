from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumPeopleGender(Enum):
    """
    性别
    """

    MALE = "男"
    FEMALE = "女"


class PeopleModel(VersionedModel):
    name: str
    gender: Optional[str]
    gender_display: Optional[str]
    born_on: Optional[datetime]
    born_on_precision: Optional[str]
    died_on: Optional[datetime]
    died_on_precision: Optional[str]
    is_verified: bool = False
    is_activated: Optional[bool] = True


class PeopleUserModel(VersionedModel):
    people_id: Optional[str]
    user_id: Optional[str]

from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumPosition(str, Enum):
    MEMBER = "成员"


class PositionModel(VersionedModel):
    name: str
    code: str

from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumValueType(Enum):
    STRING = "文本"
    JSON = "json"


class DictDataModel(VersionedModel):
    dict_meta_id: str
    name: str
    code: str
    value_type: str
    value: Optional[str]
    parent_id: Optional[str]
    seq: int = 1
    is_editable: bool = True
    is_activated: bool = True

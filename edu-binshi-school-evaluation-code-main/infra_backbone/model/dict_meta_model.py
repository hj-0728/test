from enum import Enum

from infra_basic.basic_model import VersionedModel


class DictMetaModel(VersionedModel):
    name: str
    code: str
    is_editable: bool = True
    is_activated: bool = True
    is_tree: bool = True


class EnumDictMetaCategory(Enum):
    ORGANIZATION_CATEGORY = "组织类型"

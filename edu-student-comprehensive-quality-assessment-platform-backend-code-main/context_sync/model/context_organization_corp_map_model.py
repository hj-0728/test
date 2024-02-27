from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumContextOrgCorpMapResCategory(Enum):
    """
    上下文组织关联类型
    """

    DINGTALK = "钉钉"


class ContextOrganizationCorpMapModel(VersionedModel):
    """
    上下文组织关联
    """

    organization_id: str
    res_category: str
    res_id: str

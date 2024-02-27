from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumSiteMessageContextResourceCategory(str, Enum):
    """
    资源类型
    """

    ROLE = "角色"


class EnumSiteMessageContextRelationship(str, Enum):
    """
    资源类型
    """

    UNKNOWN = "未知"


class SiteMessageContextModel(VersionedModel):
    """
    站内信上下文
    """

    site_message_id: Optional[str]
    relationship: str
    resource_category: str
    resource_id: str

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from infra_basic.basic_model import VersionedModel

from infra_backbone.model.site_message_context_model import SiteMessageContextModel


class EnumSiteMessageInitResourceCategory(str, Enum):
    """
    初始化资源类型
    """

    REPORT_RECORD = "报告记录"
    TODO_TASK = "待办事项"


class SiteMessageModel(VersionedModel):
    """
    站内信
    """

    receive_user_id: str
    send_user_id: str
    init_resource_category: str
    init_resource_id: str
    read_on: Optional[datetime]
    created_on: Optional[datetime] = None
    content: Dict
    site_message_context_list: List[SiteMessageContextModel] = []

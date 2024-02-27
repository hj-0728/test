"""
站内信
"""


from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel


class SiteMessageVm(BasicModel):
    """
    站内信
    """

    id: str
    version: Optional[int]
    receive_user_id: str
    send_user_id: str
    init_resource_category: str
    init_resource_category_name: Optional[str]
    init_resource_id: str
    read_at: Optional[datetime]
    created_at: datetime
    title: str
    content: str
    file_id: Optional[str]

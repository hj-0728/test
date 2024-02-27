from datetime import datetime
from typing import Any, Optional

from infra_basic.basic_model import VersionedModel


class AccessLogModel(VersionedModel):
    """
    访问日志
    """

    access_on: Optional[datetime]
    visitor_category: Optional[str]
    visitor_id: Optional[str]
    ip: Optional[str]
    destination: str
    args: Any
    user_agent: Optional[str]
    footprint: Any

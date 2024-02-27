from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams


class SiteMessageQueryParams(PageFilterParams):
    """
    站内信 查询对象
    """

    user_id: str
    role_id: str
    is_read: Optional[str]
    order_by: Optional[str]
    category: List[str] = []

from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class TodoTaskQueryParams(PageFilterParams):
    """
    待办事项
    """

    is_completed: Optional[bool]
    period_id: Optional[str]

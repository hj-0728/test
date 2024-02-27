from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class DingtalkK12StudentQueryParams(PageFilterParams):
    """
    学生 查询对象
    """

    wecom_user_id: Optional[str]
    wecom_k12_dept_id: Optional[str]
    period_id: Optional[str]
    get_all: bool = True

from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class DeptTreeQueryParams(PageFilterParams):
    """
    部门树 查询条件
    """

    dimension_id: Optional[str]
    user_id: Optional[str]
    get_duty_teacher_dept: bool = False
    dimension_category: Optional[str]
    dimension_code: Optional[str]

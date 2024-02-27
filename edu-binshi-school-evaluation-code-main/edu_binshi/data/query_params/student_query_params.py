from typing import Optional

from infra_basic.basic_repository import PageFilterParams


class StudentPageQueryParams(PageFilterParams):
    """
    学生 查询条件
    """

    dimension_dept_tree_id: Optional[str]
    dimension_id: Optional[str]
    user_id: Optional[str]
    get_duty_teacher_dept: bool = False

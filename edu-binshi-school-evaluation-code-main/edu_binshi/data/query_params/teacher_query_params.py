from typing import Optional, List

from infra_basic.basic_repository import PageFilterParams


class TeacherPageQueryParams(PageFilterParams):
    """
    教师 查询条件
    """

    dimension_dept_tree_id: Optional[str]
    subject_name_list: List[str] = []
    capacity_name_list: List[str] = []

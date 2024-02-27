from datetime import datetime
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class ContextDeptDetailViewModel(BasePlusModel):
    """
    上下文部门详情
    """

    id: str
    dept_id: str
    res_dept_id: str
    dept_version: int
    name: str
    comments: Optional[str]
    parent_dept_id: Optional[str]
    dimension_dept_tree_id: Optional[str]
    dimension_dept_tree_version: Optional[int]
    organization_id: str
    category_code_list: List[Optional[str]] = []

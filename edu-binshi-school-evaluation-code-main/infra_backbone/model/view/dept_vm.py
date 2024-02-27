from typing import List, Optional

from infra_basic.basic_model import BasicModel

from infra_backbone.model.dept_model import DeptModel


class DeptInfoVm(BasicModel):
    parent_not_available_count: int
    dimension_dept_tree_id: str
    organization_id: str
    name: str
    parent_id: Optional[str]
    dimension_id: str
    level: int
    seq: int
    comments: Optional[str]
    is_available: bool
    sort_info: List[str]
    path_list: List[str]


class DeptCategoryInfoVm(DeptModel):

    category_code: str

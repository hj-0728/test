from typing import Optional

from infra_basic.basic_model import BasicModel


class DimensionDeptTreeInfoVm(BasicModel):

    name: str
    code: Optional[str]
    comments: Optional[str]
    organization_id: str
    dimension_dept_tree_id: str

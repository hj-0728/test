from typing import Optional

from infra_basic.basic_model import BasePlusModel


class AddDimensionDeptEditModel(BasePlusModel):
    dimension_id: str
    organization_id: str
    name: str
    parent_dept_id: Optional[str]
    seq: int = 1

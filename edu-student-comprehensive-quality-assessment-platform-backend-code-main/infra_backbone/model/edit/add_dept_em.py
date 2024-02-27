from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class AddDeptEditModel(BasePlusModel):
    id: str
    dimension_id: Optional[str]
    dimension_category: Optional[str]
    organization_id: str
    name: str
    parent_dept_id: Optional[str]
    dept_category_id: Optional[str]
    category_code: Optional[str]
    category_name: Optional[str]
    seq: int = 1

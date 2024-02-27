from typing import Optional

from infra_basic.basic_model import BasePlusModel


class AddDeptDeptCategoryMapEditModel(BasePlusModel):
    dept_id: str
    organization_id: Optional[str]
    dept_category_id: Optional[str]
    category_code: Optional[str]
    category_name: Optional[str]

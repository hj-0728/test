from enum import Enum

from infra_basic.basic_model import VersionedModel


class DeptDeptCategoryMapModel(VersionedModel):
    dept_id: str
    dept_category_id: str

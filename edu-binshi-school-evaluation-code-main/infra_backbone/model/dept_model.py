from datetime import datetime
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel, VersionedModel

from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel


class DeptModel(VersionedModel):
    name: str
    code: Optional[str]
    comments: Optional[str]
    organization_id: str
    start_at: Optional[datetime]
    finish_at: Optional[datetime]


class EditDeptModel(VersionedModel):
    dimension_dept_tree_id: Optional[str]
    organization_id: Optional[str]
    name: str
    code: Optional[str]
    comments: Optional[str]
    dimension_id: Optional[str]
    parent_dept_id: Optional[str]
    start_at: Optional[datetime]
    finish_at: Optional[datetime]

    def to_dept_model(self):
        return DeptModel(
            name=self.name,
            code=self.code,
            comments=self.comments,
            organization_id=self.organization_id,
            start_at=self.start_at,
            finish_at=self.finish_at,
        )

    def to_dimension_dept_tree_model(self, dept_id, seq):
        return DimensionDeptTreeModel(
            dimension_id=self.dimension_id,
            dept_id=dept_id,
            parent_dept_id=self.parent_dept_id,
            seq=seq,
            start_at=self.start_at,
            finish_at=self.finish_at,
        )


class AddDeptPeopleModel(BasePlusModel):
    name: Optional[str]
    gender: Optional[str]
    dimension_dept_tree_id: str
    comments: Optional[str]
    people_id_list: List[str]

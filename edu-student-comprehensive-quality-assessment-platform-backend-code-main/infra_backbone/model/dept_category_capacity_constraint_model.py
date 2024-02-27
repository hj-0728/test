from infra_basic.basic_model import VersionedModel


class DeptCategoryCapacityConstraintModel(VersionedModel):
    dept_category_id: str
    capacity_id: str
    seq: int = 1

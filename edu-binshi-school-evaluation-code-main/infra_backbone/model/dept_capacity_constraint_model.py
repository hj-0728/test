from infra_basic.basic_model import BasePlusModel, VersionedModel


class DeptCapacityConstraintModel(VersionedModel):
    dept_id: str
    capacity_id: str
    max_size: int = 1024
    min_size: int = 1

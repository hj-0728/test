from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, text

from infra_backbone.entity.history.dept_category_capacity_constraint_history import (
    DeptCapacityCategoryConstraintHistoryEntity,
)


class DeptCategoryCapacityConstraintEntity(VersionedEntity):
    """
    部门类型Capacity约束
    """

    __tablename__ = "st_dept_category_capacity_constraint"
    __table_args__ = {"comment": "部门类型Capacity约束"}
    __history_entity__ = DeptCapacityCategoryConstraintHistoryEntity

    dept_category_id = Column(String(40), nullable=False, index=True, comment="部门类别Id")
    capacity_id = Column(String(40), nullable=False, index=True, comment="Capacity Id")
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"), index=True)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, text

from infra_backbone.entity.history.dept_capacity_constraint_history import (
    DeptCapacityConstraintHistoryEntity,
)


class DeptCapacityConstraintEntity(VersionedEntity):
    """
    部门岗位约束
    """

    __tablename__ = "st_dept_capacity_constraint"
    __table_args__ = {"comment": "团队岗位约束"}
    __history_entity__ = DeptCapacityConstraintHistoryEntity

    dept_id = Column(String(40), nullable=False, index=True, comment="团队类别id")
    capacity_id = Column(String(40), nullable=False, index=True, comment="团队职责id")
    max_size = Column(Integer, nullable=False, server_default=text("1024"), comment="最大岗位限制人数")
    min_size = Column(Integer, nullable=False, server_default=text("1"), comment="最小岗位限制人数")

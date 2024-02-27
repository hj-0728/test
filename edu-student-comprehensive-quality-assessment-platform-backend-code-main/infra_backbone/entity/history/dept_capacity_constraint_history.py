"""
部门类型   历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, text


class DeptCapacityConstraintHistoryEntity(HistoryEntity):
    """
    部门岗位约束 历史
    """

    __tablename__ = "st_dept_capacity_constraint_history"
    __table_args__ = {"comment": "部门岗位约束 历史"}

    dept_id = Column(String(40), nullable=False, index=True, comment="团队类别id")
    capacity_id = Column(String(40), nullable=False, index=True, comment="团队职责id")
    max_size = Column(Integer, nullable=False, server_default=text("1024"), comment="最大岗位限制人数")
    min_size = Column(Integer, nullable=False, server_default=text("1"), comment="最小岗位限制人数")


Index(
    "idx_dept_capacity_constraint_history_time_range",
    DeptCapacityConstraintHistoryEntity.id,
    DeptCapacityConstraintHistoryEntity.commenced_on,
    DeptCapacityConstraintHistoryEntity.ceased_on.desc(),
    unique=True,
)

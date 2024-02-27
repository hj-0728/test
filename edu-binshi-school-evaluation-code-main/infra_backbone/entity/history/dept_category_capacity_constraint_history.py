"""
部门类型   历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, text


class DeptCapacityCategoryConstraintHistoryEntity(HistoryEntity):
    """
    部门类型Capacity约束 历史
    """

    __tablename__ = "st_dept_category_capacity_constraint_history"
    __table_args__ = {"comment": "部门类型Capacity约束 历史"}

    dept_category_id = Column(String(40), nullable=False, index=True, comment="部门类别Id")
    capacity_id = Column(String(40), nullable=False, index=True, comment="Capacity Id")
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"), index=True)


Index(
    "idx_dept_capacity_category_constraint_history_time_range",
    DeptCapacityCategoryConstraintHistoryEntity.id,
    DeptCapacityCategoryConstraintHistoryEntity.begin_at,
    DeptCapacityCategoryConstraintHistoryEntity.end_at.desc(),
    unique=True,
)

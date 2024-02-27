from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String


class DimensionDeptTreeHistoryEntity(HistoryEntity):
    """
    维度树历史
    """

    __tablename__ = "st_dimension_dept_tree_history"
    __table_args__ = {"comment": "维度树历史"}

    dimension_id = Column(String(40), nullable=False, comment="维度id", index=True)
    dept_id = Column(String(40), nullable=False, comment="部门id", index=True)
    parent_dept_id = Column(String(40), nullable=True, comment="上级部门id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码", index=True)


Index(
    "idx_dimension_dept_tree_history_time_range",
    DimensionDeptTreeHistoryEntity.id,
    DimensionDeptTreeHistoryEntity.commenced_on,
    DimensionDeptTreeHistoryEntity.ceased_on.desc(),
    unique=True,
)

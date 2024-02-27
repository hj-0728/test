from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, Integer, String, text


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
    start_at = Column(DateTime(timezone=True), nullable=True, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_dimension_dept_tree_history_time_range",
    DimensionDeptTreeHistoryEntity.id,
    DimensionDeptTreeHistoryEntity.begin_at,
    DimensionDeptTreeHistoryEntity.end_at.desc(),
    unique=True,
)

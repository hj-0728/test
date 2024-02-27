"""
部门   历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class DeptHistoryEntity(HistoryEntity):
    """
    部门历史
    """

    __tablename__ = "st_dept_history"
    __table_args__ = {"comment": "部门历史"}

    organization_id = Column(String(40), comment="组织id", nullable=False)
    name = Column(String(255), nullable=False, comment="部门名称")
    code = Column(String(255), nullable=True, comment="部门编码", index=True)
    comments = Column(String(255), nullable=False, comment="描述")
    start_at = Column(DateTime(timezone=True), nullable=True, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_dept_history_time_range",
    DeptHistoryEntity.id,
    DeptHistoryEntity.begin_at,
    DeptHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class TitleAssignHistoryEntity(HistoryEntity):
    """
    抬头分配历史
    """

    __tablename__ = "st_title_assign_history"
    __table_args__ = {"comment": "抬头分配历史"}
    title_id = Column(String(40), comment="抬头id", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配id", nullable=True)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)


Index(
    "idx_title_assign_history_time_range",
    TitleAssignHistoryEntity.id,
    TitleAssignHistoryEntity.commenced_on,
    TitleAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)

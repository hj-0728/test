from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.title_assign_history import TitleAssignHistoryEntity


class TitleAssignEntity(VersionedEntity):
    """
    抬头分配
    """

    __tablename__ = "st_title_assign"
    __table_args__ = {"comment": "抬头分配"}
    __history_entity__ = TitleAssignHistoryEntity
    title_id = Column(String(40), comment="抬头id", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配id", nullable=True)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)

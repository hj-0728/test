from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.activity_history import ActivityHistoryEntity


class ActivityEntity(VersionedEntity):
    """
    活动
    """

    __tablename__ = "st_activity"
    __table_args__ = {"comment": "活动"}
    __history_entity__ = ActivityHistoryEntity
    activity_category_id = Column(String(40), comment="活动分类id", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=False)
    level = Column(String(255), comment="班/年级/校/区县/地市/省/国，可以为空", nullable=False)
    edu_holistic = Column(
        String(255), comment="教育机能（MORAL/INTELLECTUAL/PHYSICAL/AESTHETIC/LABOR）", nullable=False
    )
    status = Column(String(255), comment="状态（DRAFT/PUBLISHED/ARCHIVED/HALT）", nullable=False)

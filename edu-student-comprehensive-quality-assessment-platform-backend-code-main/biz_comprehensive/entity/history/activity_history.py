from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class ActivityHistoryEntity(HistoryEntity):
    """
    活动历史
    """

    __tablename__ = "st_activity_history"
    __table_args__ = {"comment": "活动历史"}
    activity_category_id = Column(String(40), comment="活动分类id", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=False)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=False)
    level = Column(String(255), comment="班/年级/校/区县/地市/省/国，可以为空", nullable=False)
    edu_holistic = Column(
        String(255), comment="教育机能（MORAL/INTELLECTUAL/PHYSICAL/AESTHETIC/LABOR）", nullable=False
    )
    status = Column(String(255), comment="状态（DRAFT/PUBLISHED/ARCHIVED/HALT）", nullable=False)


Index(
    "idx_activity_history_time_range",
    ActivityHistoryEntity.id,
    ActivityHistoryEntity.commenced_on,
    ActivityHistoryEntity.ceased_on.desc(),
    unique=True,
)

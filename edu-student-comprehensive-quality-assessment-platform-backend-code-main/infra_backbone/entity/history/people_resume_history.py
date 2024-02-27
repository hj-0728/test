from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, Text


class PeopleResumeHistoryEntity(HistoryEntity):
    """
    人员履历历史
    """

    __tablename__ = "st_people_resume_history"
    __table_args__ = {"comment": "人员履历历史"}

    people_id = Column(String(40), nullable=False, comment="人员id")
    started_on = Column(DateTime(timezone=True), nullable=True, comment="开始日期")
    started_on_precision = Column(String(255), nullable=True, comment="开始时间精度（年、月、日）")
    ended_on = Column(DateTime(timezone=True), nullable=True, comment="结束日期")
    ended_on_precision = Column(String(255), nullable=True, comment="结束时间精度（年、月、日）")
    address_id = Column(String(40), nullable=True, comment="地址id")
    organization_id = Column(String(40), nullable=True, comment="单位id")
    affairs_code = Column(String(255), nullable=False, comment="所做事务类型，用枚举罗列")
    comments = Column(Text, nullable=False, comment="备注")


Index(
    "idx_people_resume_history_time_range",
    PeopleResumeHistoryEntity.id,
    PeopleResumeHistoryEntity.commenced_on,
    PeopleResumeHistoryEntity.ceased_on.desc(),
    unique=True,
)

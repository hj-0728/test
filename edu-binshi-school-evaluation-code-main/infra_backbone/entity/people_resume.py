from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, Text

from infra_backbone.entity.history.people_resume_history import PeopleResumeHistoryEntity


class PeopleResumeEntity(VersionedEntity):
    """
    人员履历
    """

    __tablename__ = "st_people_resume"
    __table_args__ = {"comment": "人员履历"}
    __history_entity__ = PeopleResumeHistoryEntity

    people_id = Column(String(40), nullable=False, comment="人员id")
    start_at = Column(DateTime(timezone=True), nullable=True, comment="开始日期")
    start_at_precision = Column(String(255), nullable=True, comment="开始时间精度（年、月、日）")
    finish_at = Column(DateTime(timezone=True), nullable=True, comment="结束日期")
    finish_at_precision = Column(String(255), nullable=True, comment="结束时间精度（年、月、日）")
    address_id = Column(String(40), nullable=True, comment="地址id", index=True)
    organization_id = Column(String(40), nullable=True, comment="单位id", index=True)
    affairs_code = Column(String(255), nullable=False, comment="所做事务类型，用枚举罗列", index=True)
    comments = Column(Text, nullable=False, comment="备注")

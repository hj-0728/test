from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, DateTime, String, text

from infra_backbone.entity.history.people_history import PeopleHistoryEntity


class PeopleEntity(VersionedEntity):
    """
    人员
    """

    __tablename__ = "st_people"
    __table_args__ = {"comment": "人员"}
    __history_entity__ = PeopleHistoryEntity

    name = Column(String(255), nullable=False, comment="姓名", index=True)
    gender = Column(String(255), nullable=True, comment="性别")
    born_at = Column(DateTime(timezone=True), nullable=True, comment="出生日期")
    born_at_precision = Column(String(255), nullable=True, comment="出生时间精度（年、月、日）")
    died_at = Column(DateTime(timezone=True), nullable=True, comment="死亡日期")
    died_at_precision = Column(String(255), nullable=True, comment="死亡时间精度（年、月、日）")
    is_verified = Column(Boolean, nullable=False, comment="是否验证", server_default=text("false"))
    is_available = Column(Boolean, nullable=False, comment="是否可用", server_default=text("true"))

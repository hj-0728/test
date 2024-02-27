from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.awarding_history import AwardingHistoryEntity


class AwardingEntity(VersionedEntity):
    """
    荣誉
    """

    __tablename__ = "st_awarding"
    __table_args__ = {"comment": "荣誉"}
    __history_entity__ = AwardingHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    level = Column(
        String(255), comment="级别（NATION/PROVINCE/CITY/DISTRICT/SCHOOL/GRADE/CLASS）", nullable=True
    )

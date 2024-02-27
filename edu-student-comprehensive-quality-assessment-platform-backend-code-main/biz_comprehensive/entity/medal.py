from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.medal_history import MedalHistoryEntity


class MedalEntity(VersionedEntity):
    """
    勋章
    """

    __tablename__ = "st_medal"
    __table_args__ = {"comment": "勋章"}
    __history_entity__ = MedalHistoryEntity
    name = Column(String(255), comment="勋章名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    level = Column(String(255), comment="级别（SCHOOL/GRADE/CLASS）", nullable=False)

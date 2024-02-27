from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class MedalHistoryEntity(HistoryEntity):
    """
    勋章历史
    """

    __tablename__ = "st_medal_history"
    __table_args__ = {"comment": "勋章历史"}
    name = Column(String(255), comment="勋章名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    level = Column(String(255), comment="级别（SCHOOL/GRADE/CLASS）", nullable=False)


Index(
    "idx_medal_history_time_range",
    MedalHistoryEntity.id,
    MedalHistoryEntity.commenced_on,
    MedalHistoryEntity.ceased_on.desc(),
    unique=True,
)

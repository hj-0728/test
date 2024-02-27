from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AwardingHistoryEntity(HistoryEntity):
    """
    荣誉历史
    """

    __tablename__ = "st_awarding_history"
    __table_args__ = {"comment": "荣誉历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    level = Column(
        String(255), comment="级别（NATION/PROVINCE/CITY/DISTRICT/SCHOOL/GRADE/CLASS）", nullable=True
    )


Index(
    "idx_awarding_history_time_range",
    AwardingHistoryEntity.id,
    AwardingHistoryEntity.commenced_on,
    AwardingHistoryEntity.ceased_on.desc(),
    unique=True,
)

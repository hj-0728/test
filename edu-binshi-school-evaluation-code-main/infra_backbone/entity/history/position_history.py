from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class PositionHistoryEntity(HistoryEntity):
    """
    职位  历史实体类
    """

    __tablename__ = "st_position_history"
    __table_args__ = {"comment": "职位"}

    name = Column(String(255), nullable=False, comment="职位名称")
    code = Column(String(255), nullable=False, comment="职位编码")


Index(
    "idx_position_history_time_range",
    PositionHistoryEntity.id,
    PositionHistoryEntity.begin_at,
    PositionHistoryEntity.end_at.desc(),
    unique=True,
)

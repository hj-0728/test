from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, text


class CapacityHistoryEntity(HistoryEntity):
    """
    特定环境或情境中的角色和功能
    """

    __tablename__ = "st_capacity_history"
    __table_args__ = {"comment": "特定环境或情境中的角色和功能"}

    name = Column(String(40), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
    is_available = Column(Boolean, nullable=False, comment="是否可用", server_default=text("true"))


Index(
    "idx_capacity_history_time_range",
    CapacityHistoryEntity.id,
    CapacityHistoryEntity.begin_at,
    CapacityHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.capacity_history import CapacityHistoryEntity


class CapacityEntity(VersionedEntity):
    """
    特定环境或情境中的角色和功能
    """

    __tablename__ = "st_capacity"
    __table_args__ = {"comment": "特定环境或情境中的角色和功能"}
    __history_entity__ = CapacityHistoryEntity

    name = Column(String(40), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
    is_activated = Column(Boolean, nullable=False, comment="是否可用", server_default=text("true"))

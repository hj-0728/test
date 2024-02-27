from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.position_history import PositionHistoryEntity


class PositionEntity(VersionedEntity):
    """
    职位
    """

    __tablename__ = "st_position"
    __table_args__ = {"comment": "职位"}
    __history_entity__ = PositionHistoryEntity

    name = Column(String(255), nullable=False, comment="职位名称")
    code = Column(String(255), nullable=False, comment="职位编码", unique=True, index=True)

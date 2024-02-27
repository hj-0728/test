from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.area_history import AreaHistoryEntity


class AreaEntity(VersionedEntity):
    """
    行政区划
    """

    __tablename__ = "st_area"
    __table_args__ = {"comment": "行政区划"}
    __history_entity__ = AreaHistoryEntity

    parent_id = Column(String(40), nullable=True, comment="父id，空的为根节点", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    zoning_code = Column(String(255), nullable=True, comment="行政区划代码", index=True, unique=True)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, Integer, String

from infra_backbone.entity.history.access_resource_set_detail_history import (
    AccessResourceSetDetailHistoryEntity,
)


class AccessResourceSetDetailEntity(VersionedEntity):
    """
    访问资源集合详情
    """

    __tablename__ = "st_access_resource_set_detail"
    __table_args__ = {"comment": "访问资源集合详情"}
    __history_entity__ = AccessResourceSetDetailHistoryEntity

    access_resource_set_id = Column(String(40), nullable=False, comment="前端路径id", index=True)
    bind_resource_category = Column(String(40), nullable=False, comment="绑定资源类别")
    bind_resource_id = Column(Integer, nullable=False, comment="绑定资源id")


Index(
    "idx_access_resource_set_detail_resource_info",
    AccessResourceSetDetailEntity.bind_resource_category,
    AccessResourceSetDetailEntity.bind_resource_id,
)

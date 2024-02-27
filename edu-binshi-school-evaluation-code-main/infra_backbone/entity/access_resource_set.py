from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.access_resource_set_history import AccessResourceSetHistoryEntity


class AccessResourceSetEntity(VersionedEntity):
    """
    访问资源集合
    """

    __tablename__ = "st_access_resource_set"
    __table_args__ = {"comment": "访问资源集合"}
    __history_entity__ = AccessResourceSetHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)

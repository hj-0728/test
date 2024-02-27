from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.identity_number_history import IdentityNumberHistoryEntity


class IdentityNumberEntity(VersionedEntity):
    """
    身份编号
    """

    __tablename__ = "st_identity_number"
    __table_args__ = {"comment": "身份编号"}
    __history_entity__ = IdentityNumberHistoryEntity

    owner_id = Column(String(40), nullable=False, comment="拥有者id")
    owner_category = Column(String(255), nullable=False, comment="拥有者类型")
    category = Column(String(255), nullable=False, comment="类型", index=True)
    number = Column(String(255), nullable=False, comment="编号")


Index(
    "idx_identity_number_resource_info",
    IdentityNumberEntity.owner_category,
    IdentityNumberEntity.owner_id,
)

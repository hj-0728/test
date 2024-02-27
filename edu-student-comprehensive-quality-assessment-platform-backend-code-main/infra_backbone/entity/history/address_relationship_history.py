from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AddressRelationshipHistoryEntity(HistoryEntity):
    """
    地址关系历史
    """

    __tablename__ = "st_address_relationship_history"
    __table_args__ = {"comment": "地址关系历史"}

    address_id = Column(String(40), nullable=False, comment="地址id", index=True)
    resource_category = Column(String(255), nullable=False, comment="资源类别")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    relationship = Column(String(255), nullable=False, comment="关系", index=True)


Index(
    "idx_address_relationship_history_time_range",
    AddressRelationshipHistoryEntity.id,
    AddressRelationshipHistoryEntity.commenced_on,
    AddressRelationshipHistoryEntity.ceased_on.desc(),
    unique=True,
)

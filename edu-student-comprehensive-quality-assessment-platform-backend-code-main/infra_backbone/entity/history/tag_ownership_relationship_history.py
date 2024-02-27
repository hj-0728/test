from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class TagOwnershipRelationshipHistoryEntity(HistoryEntity):
    """
    标签所属关系历史
    """

    __tablename__ = "st_tag_ownership_relationship_history"
    __table_args__ = {"comment": "标签所属关系历史"}

    tag_ownership_id = Column(String(40), nullable=False, comment="标签所属id")
    resource_category = Column(String(255), nullable=False, comment="资源类型")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    relationship = Column(String(255), nullable=False, comment="关系")


Index(
    "idx_tag_ownership_relationship_history_time_range",
    TagOwnershipRelationshipHistoryEntity.id,
    TagOwnershipRelationshipHistoryEntity.commenced_on,
    TagOwnershipRelationshipHistoryEntity.ceased_on.desc(),
    unique=True,
)


Index(
    "idx_tag_ownership_relationship_history_resource_info",
    TagOwnershipRelationshipHistoryEntity.resource_category,
    TagOwnershipRelationshipHistoryEntity.resource_id,
)

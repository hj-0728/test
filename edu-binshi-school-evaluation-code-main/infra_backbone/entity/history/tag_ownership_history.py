"""
标签所属  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String


class TagOwnershipHistoryEntity(HistoryEntity):
    """
    标签所属历史
    """

    __tablename__ = "st_tag_ownership_history"
    __table_args__ = {"comment": "标签所属历史"}

    tag_id = Column(String(40), nullable=False, comment="标签id", index=True)
    code = Column(String(255), nullable=True, comment="编码", index=True)
    owner_category = Column(String(255), nullable=False, comment="所属类型")
    owner_id = Column(String(40), nullable=False, comment="所属id")
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑")
    is_activated = Column(Boolean, nullable=False, comment="是否激活")


Index(
    "idx_tag_ownership_history_time_range",
    TagOwnershipHistoryEntity.id,
    TagOwnershipHistoryEntity.begin_at,
    TagOwnershipHistoryEntity.end_at.desc(),
    unique=True,
)

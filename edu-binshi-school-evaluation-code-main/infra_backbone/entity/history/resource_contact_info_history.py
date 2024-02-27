from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ResourceContactInfoHistoryEntity(HistoryEntity):
    """
    资源联系方式历史
    """

    __tablename__ = "st_resource_contact_info_history"
    __table_args__ = {"comment": "资源联系方式历史"}

    resource_category = Column(String(255), nullable=False, comment="资源类型")
    resource_id = Column(String(40), nullable=False, comment="资源id")
    contact_info_id = Column(String(40), nullable=False, comment="联系方式id", index=True)


Index(
    "idx_resource_contact_info_history_time_range",
    ResourceContactInfoHistoryEntity.id,
    ResourceContactInfoHistoryEntity.begin_at,
    ResourceContactInfoHistoryEntity.end_at.desc(),
    unique=True,
)

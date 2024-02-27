"""
组织  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String


class OrganizationHistoryEntity(HistoryEntity):
    """
    组织  历史实体类
    """

    __tablename__ = "st_organization_history"
    __table_args__ = {"comment": "组织"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=True, comment="编码", index=True)
    category = Column(String(255), nullable=True, comment="类型", index=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活")


Index(
    "idx_organization_history_time_range",
    OrganizationHistoryEntity.id,
    OrganizationHistoryEntity.begin_at,
    OrganizationHistoryEntity.end_at.desc(),
    unique=True,
)

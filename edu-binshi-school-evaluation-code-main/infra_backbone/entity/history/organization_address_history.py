from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String

from infra_backbone.entity.history.organization_history import OrganizationHistoryEntity


class OrganizationAddressHistoryEntity(HistoryEntity):
    """
    组织地址历史
    """

    __tablename__ = "st_organization_address_history"
    __table_args__ = {"comment": "组织地址历史"}
    __history_entity__ = OrganizationHistoryEntity

    organization_id = Column(String(40), nullable=False, comment="组织id")
    address_id = Column(String(40), nullable=False, comment="地址id")
    seq = Column(Integer, nullable=False, comment="排序码")


Index(
    "idx_organization_address_history_time_range",
    OrganizationAddressHistoryEntity.id,
    OrganizationAddressHistoryEntity.begin_at,
    OrganizationAddressHistoryEntity.end_at.desc(),
    unique=True,
)

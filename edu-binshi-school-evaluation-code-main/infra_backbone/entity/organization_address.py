from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String

from infra_backbone.entity.history.organization_address_history import (
    OrganizationAddressHistoryEntity,
)


class OrganizationAddressEntity(VersionedEntity):
    """
    组织地址
    """

    __tablename__ = "st_organization_address"
    __table_args__ = {"comment": "组织地址"}
    __history_entity__ = OrganizationAddressHistoryEntity

    organization_id = Column(String(40), nullable=False, comment="组织id")
    address_id = Column(String(40), nullable=False, comment="地址id")
    seq = Column(Integer, nullable=False, comment="排序码")

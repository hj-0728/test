"""
上下文组织关联
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from context_sync.entity.history.context_organization_corp_map_history import (
    ContextOrganizationCorpMapHistoryEntity,
)


class ContextOrganizationCorpMapEntity(VersionedEntity):
    """
    上下文组织关联
    """

    __tablename__ = "st_context_organization_corp_map"
    __table_args__ = {"comment": "上下文组织关联"}
    __history_entity__ = ContextOrganizationCorpMapHistoryEntity
    organization_id = Column(String(40), comment="组织id", nullable=False)
    res_category = Column(String(255), comment="关联corp类型", nullable=False)
    res_id = Column(String(40), comment="关联corpid", nullable=True)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.organization_history import OrganizationHistoryEntity


class OrganizationEntity(VersionedEntity):
    """
    组织
    """

    __tablename__ = "st_organization"
    __table_args__ = {"comment": "组织"}
    __history_entity__ = OrganizationHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=True, comment="编码", index=True)
    category = Column(String(255), nullable=False, comment="类型", index=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))

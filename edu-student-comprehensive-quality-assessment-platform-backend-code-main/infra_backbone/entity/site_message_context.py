from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, UniqueConstraint

from infra_backbone.entity.history.site_message_context_history import (
    SiteMessageContextHistoryEntity,
)


class SiteMessageContextEntity(VersionedEntity):
    """
    站内信上下文
    """

    __tablename__ = "st_site_message_context"
    __table_args__ = (
        UniqueConstraint(
            "site_message_id",
            "relationship",
            "resource_category",
            "resource_id",
            name="uc_site_message_context",
        ),
        {"comment": "站内信上下文"},
    )
    __history_entity__ = SiteMessageContextHistoryEntity
    site_message_id = Column(String(40), comment="站内信id", nullable=False, index=True)
    relationship = Column(String(255), comment="关系", nullable=False)
    resource_category = Column(String(255), comment="资源类型", nullable=False)
    resource_id = Column(String(40), comment="资源id", nullable=False)

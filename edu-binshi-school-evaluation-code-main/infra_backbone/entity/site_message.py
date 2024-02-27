from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, func, Index, String
from sqlalchemy.dialects.postgresql import JSONB

from infra_backbone.entity.history.site_message_history import SiteMessageHistoryEntity


class SiteMessageEntity(VersionedEntity):
    """
    站内信
    """

    __tablename__ = "st_site_message"
    __table_args__ = {"comment": "站内信"}
    __history_entity__ = SiteMessageHistoryEntity
    receive_user_id = Column(String(40), nullable=False, comment="接收用户id", index=True)
    send_user_id = Column(String(40), nullable=False, comment="发送用户id", index=True)
    init_resource_category = Column(String(255), comment="初始化资源类型", nullable=False)
    init_resource_id = Column(String(40), comment="初始化资源id", nullable=False)
    read_at = Column(
        DateTime(timezone=True),
        comment="阅读于",
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        comment="创建于",
        server_default=func.now(),
        nullable=False,
    )
    content = Column(JSONB, comment="内容", nullable=False)


Index(
    "idx_site_message_resource",
    SiteMessageEntity.init_resource_category,
    SiteMessageEntity.init_resource_id,
)

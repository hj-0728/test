from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB


class SiteMessageHistoryEntity(HistoryEntity):
    """
    站内信 历史
    """

    __tablename__ = "st_site_message_history"
    __table_args__ = {"comment": "站内信 历史"}
    receive_user_id = Column(String(40), nullable=False, comment="接收用户id", index=True)
    send_user_id = Column(String(40), nullable=False, comment="发送用户id", index=True)
    init_resource_category = Column(String(255), comment="初始化资源类型", nullable=False)
    init_resource_id = Column(String(40), comment="初始化资源id", nullable=False)
    read_on = Column(
        DateTime(timezone=True),
        comment="阅读于",
        nullable=True,
    )
    created_on = Column(
        DateTime(timezone=True),
        comment="创建于",
        nullable=False,
    )
    content = Column(JSONB, comment="内容", nullable=False)


Index(
    "idx_site_message_history_time_range",
    SiteMessageHistoryEntity.id,
    SiteMessageHistoryEntity.commenced_on,
    SiteMessageHistoryEntity.ceased_on.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SiteMessageContextHistoryEntity(HistoryEntity):
    """
    站内信上下文
    """

    __tablename__ = "st_site_message_context_history"
    __table_args__ = {"comment": "站内信上下文历史"}
    site_message_id = Column(String(40), nullable=False, comment="站内信id", index=True)
    relationship = Column(String(255), nullable=False, comment="关系")
    resource_category = Column(String(255), comment="资源类型", nullable=False)
    resource_id = Column(String(40), comment="资源id", nullable=False)


Index(
    "idx_site_message_context_history_time_range",
    SiteMessageContextHistoryEntity.id,
    SiteMessageContextHistoryEntity.begin_at,
    SiteMessageContextHistoryEntity.end_at.desc(),
    unique=True,
)

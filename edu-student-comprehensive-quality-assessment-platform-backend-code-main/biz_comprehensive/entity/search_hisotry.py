from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String

from biz_comprehensive.entity.history.search_history_history import SearchHistoryHistoryEntity


class SearchHistoryEntity(VersionedEntity):
    """
    搜索历史
    """

    __tablename__ = "st_search_history"
    __table_args__ = {"comment": "搜索历史"}
    __history_entity__ = SearchHistoryHistoryEntity
    owner_people_id = Column(String(40), comment="拥有者人员id", nullable=False)
    search_content = Column(String(255), comment="搜索内容", nullable=False)
    search_on = Column(DateTime(timezone=True), comment="搜索时间", nullable=False)
    search_scene = Column(String(255), comment="搜索场景（用枚举表示，MOBILE_STUDENT）", nullable=False)

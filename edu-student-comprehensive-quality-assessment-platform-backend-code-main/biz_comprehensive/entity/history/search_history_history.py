from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class SearchHistoryHistoryEntity(HistoryEntity):
    """
    搜索历史历史
    """

    __tablename__ = "st_search_history_history"
    __table_args__ = {"comment": "搜索历史历史"}
    owner_people_id = Column(String(40), comment="拥有者人员id", nullable=False)
    search_content = Column(String(255), comment="搜索内容", nullable=False)
    search_on = Column(DateTime(timezone=True), comment="搜索时间", nullable=False)
    search_scene = Column(String(255), comment="搜索场景（用枚举表示，MOBILE_STUDENT）", nullable=False)


Index(
    "idx_search_history_history_time_range",
    SearchHistoryHistoryEntity.id,
    SearchHistoryHistoryEntity.commenced_on,
    SearchHistoryHistoryEntity.ceased_on.desc(),
    unique=True,
)

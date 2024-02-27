from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String


class ActivityCategoryHistoryEntity(HistoryEntity):
    """
    活动分类历史
    """

    __tablename__ = "st_activity_category_history"
    __table_args__ = {"comment": "活动分类历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    is_activated = Column(Boolean, comment="是否启用", nullable=False)


Index(
    "idx_activity_category_history_time_range",
    ActivityCategoryHistoryEntity.id,
    ActivityCategoryHistoryEntity.commenced_on,
    ActivityCategoryHistoryEntity.ceased_on.desc(),
    unique=True,
)

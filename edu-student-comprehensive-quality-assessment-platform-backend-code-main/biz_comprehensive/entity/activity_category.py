from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String

from biz_comprehensive.entity.history.activity_category_history import ActivityCategoryHistoryEntity


class ActivityCategoryEntity(VersionedEntity):
    """
    活动分类
    """

    __tablename__ = "st_activity_category"
    __table_args__ = {"comment": "活动分类"}
    __history_entity__ = ActivityCategoryHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    is_activated = Column(Boolean, comment="是否启用", nullable=False)

"""
上下文人和用户关联历史
"""

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ContextPeopleUserMapHistoryEntity(HistoryEntity):
    """
    上下文人和用户关联历史
    """

    __tablename__ = "st_context_people_user_map_history"
    __table_args__ = {"comment": "上下文人和用户关联历史"}

    people_id = Column(String(40), comment="人的id", nullable=False)
    res_category = Column(String(255), comment="关联用户类型", nullable=False)
    res_id = Column(String(40), comment="关联用户id", nullable=True)


Index(
    "idx_context_people_user_map_history_time_range",
    ContextPeopleUserMapHistoryEntity.id,
    ContextPeopleUserMapHistoryEntity.commenced_on,
    ContextPeopleUserMapHistoryEntity.ceased_on.desc(),
    unique=True,
)

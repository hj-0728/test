"""
上下文人和用户关联
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from context_sync.entity.history.context_people_user_map_history import (
    ContextPeopleUserMapHistoryEntity,
)


class ContextPeopleUserMapEntity(VersionedEntity):
    """
    上下文人和用户关联
    """

    __tablename__ = "st_context_people_user_map"
    __table_args__ = {"comment": "上下文人和用户关联"}
    __history_entity__ = ContextPeopleUserMapHistoryEntity
    people_id = Column(String(40), comment="人的id", nullable=False)
    res_category = Column(String(255), comment="关联用户类型", nullable=False)
    res_id = Column(String(40), comment="关联用户id", nullable=True)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.people_user_history import PeopleUserHistoryEntity


class PeopleUserEntity(VersionedEntity):
    """
    人员用户
    """

    __tablename__ = "st_people_user"
    __table_args__ = {"comment": "人员用户"}
    __history_entity__ = PeopleUserHistoryEntity

    people_id = Column(String(40), nullable=False, comment="人员id", index=True)
    user_id = Column(String(40), nullable=False, comment="用户id", index=True)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class PeopleUserHistoryEntity(HistoryEntity):
    """
    人员用户历史
    """

    __tablename__ = "st_people_user_history"
    __table_args__ = {"comment": "人员用户"}

    people_id = Column(String(40), nullable=False, comment="人员id")
    user_id = Column(String(40), nullable=False, comment="用户id")


Index(
    "idx_people_user_history_time_range",
    PeopleUserHistoryEntity.id,
    PeopleUserHistoryEntity.begin_at,
    PeopleUserHistoryEntity.end_at.desc(),
    unique=True,
)

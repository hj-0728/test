from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, text

from infra_backbone.entity.history.team_goal_history import TeamGoalHistoryEntity


class TeamGoalEntity(VersionedEntity):
    """
    小组目标
    """

    __tablename__ = "st_team_goal"
    __table_args__ = {"comment": "小组目标"}
    __history_entity__ = TeamGoalHistoryEntity

    team_id = Column(String(40), nullable=False, comment="小组id", index=True)
    goal_category = Column(String(255), nullable=False, comment="目标类型")
    goal_id = Column(String(40), nullable=False, comment="目标id", index=True)
    activity = Column(String(255), nullable=False, comment="活动")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间",
        server_default=text("'infinity'::timestamptz"),
    )

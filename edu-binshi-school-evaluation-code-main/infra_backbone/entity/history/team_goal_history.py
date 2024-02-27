from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class TeamGoalHistoryEntity(HistoryEntity):
    """
    小组目标历史
    """

    __tablename__ = "st_team_goal_history"
    __table_args__ = {"comment": "小组目标（历史）"}

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


Index(
    "idx_team_goal_history_time_range",
    TeamGoalHistoryEntity.id,
    TeamGoalHistoryEntity.begin_at,
    TeamGoalHistoryEntity.end_at.desc(),
    unique=True,
)

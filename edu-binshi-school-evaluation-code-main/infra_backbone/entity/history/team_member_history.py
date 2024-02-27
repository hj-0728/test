from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, Integer, String, text


class TeamMemberHistoryEntity(HistoryEntity):
    """
    小组成员历史
    """

    __tablename__ = "st_team_member_history"
    __table_args__ = {"comment": "小组成员（历史）"}

    team_id = Column(String(40), nullable=False, comment="小组id", index=True)
    people_id = Column(String(40), nullable=False, comment="人员id", index=True)
    capacity_id = Column(String(40), nullable=False, comment="职能id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间",
        server_default=text("'infinity'::timestamp without time zone"),
    )


Index(
    "idx_team_member_history_time_range",
    TeamMemberHistoryEntity.id,
    TeamMemberHistoryEntity.begin_at,
    TeamMemberHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class TeamHistoryEntity(HistoryEntity):
    """
    小组历史
    """

    __tablename__ = "st_team_history"
    __table_args__ = {"comment": "小组(历史)"}

    team_category_id = Column(String(40), nullable=False, comment="小组类型id", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间",
        server_default=text("'infinity'::timestamp without time zone"),
    )


Index(
    "idx_team_history_time_range",
    TeamHistoryEntity.id,
    TeamHistoryEntity.begin_at,
    TeamHistoryEntity.end_at.desc(),
    unique=True,
)

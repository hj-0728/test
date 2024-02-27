from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, text

from infra_backbone.entity.history.team_history import TeamHistoryEntity


class TeamEntity(VersionedEntity):
    """
    小组
    """

    __tablename__ = "st_team"
    __table_args__ = {"comment": "小组"}
    __history_entity__ = TeamHistoryEntity

    team_category_id = Column(String(40), nullable=False, comment="小组类型id", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间",
        server_default=text("'infinity'::timestamp without time zone"),
    )

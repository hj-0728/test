from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Integer, String, text

from infra_backbone.entity.history.team_member_history import TeamMemberHistoryEntity


class TeamMemberEntity(VersionedEntity):
    """
    小组成员
    """

    __tablename__ = "st_team_member"
    __table_args__ = {"comment": "小组成员"}
    __history_entity__ = TeamMemberHistoryEntity

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

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ClassTeamMemberHistoryEntity(HistoryEntity):
    """
    班级小组成员历史
    """

    __tablename__ = "st_class_team_member_history"
    __table_args__ = {"comment": "班级小组成员历史"}
    class_team_id = Column(String(40), comment="班级小组id", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配的id", nullable=False)


Index(
    "idx_class_team_member_history_time_range",
    ClassTeamMemberHistoryEntity.id,
    ClassTeamMemberHistoryEntity.commenced_on,
    ClassTeamMemberHistoryEntity.ceased_on.desc(),
    unique=True,
)

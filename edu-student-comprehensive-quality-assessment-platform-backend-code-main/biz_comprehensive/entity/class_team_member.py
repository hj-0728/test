from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.class_team_member_history import ClassTeamMemberHistoryEntity


class ClassTeamMemberEntity(VersionedEntity):
    """
    班级小组成员
    """

    __tablename__ = "st_class_team_member"
    __table_args__ = {"comment": "班级小组成员"}
    __history_entity__ = ClassTeamMemberHistoryEntity
    class_team_id = Column(String(40), comment="班级小组id", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配的id", nullable=False)

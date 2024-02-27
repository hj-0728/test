from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.class_team_history import ClassTeamHistoryEntity


class ClassTeamEntity(VersionedEntity):
    """
    班级小组
    """

    __tablename__ = "st_class_team"
    __table_args__ = {"comment": "班级小组"}
    __history_entity__ = ClassTeamHistoryEntity
    class_team_category_id = Column(String(40), comment="班级小组类型id", nullable=False)
    name = Column(String(255), comment="小组名称", nullable=False)
    creator_people_id = Column(String(40), comment="创建者id", nullable=False)

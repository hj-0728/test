from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ClassTeamHistoryEntity(HistoryEntity):
    """
    班级小组历史
    """

    __tablename__ = "st_class_team_history"
    __table_args__ = {"comment": "班级小组历史"}
    class_team_category_id = Column(String(40), comment="班级小组类型id", nullable=False)
    name = Column(String(255), comment="小组名称", nullable=False)
    creator_people_id = Column(String(40), comment="创建者id", nullable=False)


Index(
    "idx_class_team_history_time_range",
    ClassTeamHistoryEntity.id,
    ClassTeamHistoryEntity.commenced_on,
    ClassTeamHistoryEntity.ceased_on.desc(),
    unique=True,
)

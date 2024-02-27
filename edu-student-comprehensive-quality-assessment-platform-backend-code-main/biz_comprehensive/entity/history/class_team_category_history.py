from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ClassTeamCategoryHistoryEntity(HistoryEntity):
    """
    班级小组类型历史
    """

    __tablename__ = "st_class_team_category_history"
    __table_args__ = {"comment": "班级小组类型历史"}
    name = Column(String(255), comment="小组类型名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    dimension_dept_tree_id = Column(String(40), comment="部门范围id", nullable=False)
    creator_people_id = Column(String(40), comment="创建人id", nullable=False)


Index(
    "idx_class_team_category_history_time_range",
    ClassTeamCategoryHistoryEntity.id,
    ClassTeamCategoryHistoryEntity.commenced_on,
    ClassTeamCategoryHistoryEntity.ceased_on.desc(),
    unique=True,
)

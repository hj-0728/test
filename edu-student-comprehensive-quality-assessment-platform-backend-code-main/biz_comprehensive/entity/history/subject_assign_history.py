from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SubjectAssignHistoryEntity(HistoryEntity):
    """
    科目分配历史
    """

    __tablename__ = "st_subject_assign_history"
    __table_args__ = {"comment": "科目分配历史"}
    subject_id = Column(String(40), comment="科目id", nullable=False)
    dimension_dept_tree_id = Column(String(40), comment="部门维度树id", nullable=False)
    teacher_id = Column(String(40), comment="教师id", nullable=False)


Index(
    "idx_subject_assign_history_time_range",
    SubjectAssignHistoryEntity.id,
    SubjectAssignHistoryEntity.commenced_on,
    SubjectAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)

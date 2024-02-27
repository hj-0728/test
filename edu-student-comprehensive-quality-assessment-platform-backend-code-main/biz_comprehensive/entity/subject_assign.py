from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.subject_assign_history import SubjectAssignHistoryEntity


class SubjectAssignEntity(VersionedEntity):
    """
    科目分配
    """

    __tablename__ = "st_subject_assign"
    __table_args__ = {"comment": "科目分配"}
    __history_entity__ = SubjectAssignHistoryEntity
    subject_id = Column(String(40), comment="科目id", nullable=False)
    dimension_dept_tree_id = Column(String(40), comment="部门维度树id", nullable=False)
    teacher_id = Column(String(40), comment="教师id", nullable=False)

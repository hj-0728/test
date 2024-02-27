"""
教师科目实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, text

from edu_binshi.entity.history.k12_teacher_subject_history import K12TeacherSubjectHistoryEntity


class K12TeacherSubjectEntity(VersionedEntity):
    """
    周期
    """

    __tablename__ = "st_k12_teacher_subject"
    __table_args__ = {"comment": "k12教师科目"}
    __history_entity__ = K12TeacherSubjectHistoryEntity
    people_id = Column(String(40), comment="人员id", nullable=False, index=True)
    dimension_dept_tree_id = Column(String(40), comment="部门树id", nullable=False, index=True)
    subject_id = Column(String(40), comment="科目id", nullable=False)
    start_at = Column(DateTime(timezone=True), comment="开始于", nullable=False)
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )

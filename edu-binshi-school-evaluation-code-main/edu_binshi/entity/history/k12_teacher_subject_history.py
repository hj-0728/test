"""
周期历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class K12TeacherSubjectHistoryEntity(HistoryEntity):
    """
    k12教师科目（历史实体类）
    """

    __tablename__ = "st_k12_teacher_subject_history"
    __table_args__ = {"comment": "k12教师科目（历史）"}
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


Index(
    "idx_k12_teacher_subject_history_time_range",
    K12TeacherSubjectHistoryEntity.id,
    K12TeacherSubjectHistoryEntity.begin_at,
    K12TeacherSubjectHistoryEntity.end_at.desc(),
    unique=True,
)

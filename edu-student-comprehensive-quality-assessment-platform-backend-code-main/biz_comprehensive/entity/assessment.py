from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import ARRAY, Column, DateTime, Integer, Numeric, String

from biz_comprehensive.entity.history.assessment_history import AssessmentHistoryEntity


class AssessmentEntity(VersionedEntity):
    """
    评估
    """

    __tablename__ = "st_assessment"
    __table_args__ = {"comment": "评估"}
    __history_entity__ = AssessmentHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    assessment_category = Column(String(255), comment="评估类别（EXAM/QUIZ/HOMEWORK）", nullable=False)
    subject_id = Column(String(40), comment="科目id", nullable=False)
    started_on = Column(DateTime(timezone=True), comment="开始时间", nullable=True)
    ended_on = Column(DateTime(timezone=True), comment="结束时间", nullable=True)
    result_value_type = Column(String(255), comment="结果值类型（NUM/STRING）", nullable=False)
    numeric_precision = Column(Integer, comment="精度", nullable=True)
    numeric_max = Column(Numeric, comment="数值最大值", nullable=True)
    string_options = Column(ARRAY(String(255)), comment="字符可选项", nullable=True)
    period_id = Column(String(40), comment="学期id", nullable=False)
    assessment_level = Column(String(255), comment="评估级别（NORMAL/MIDTERM/FINAL）", nullable=False)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import ARRAY, Column, DateTime, Index, Integer, Numeric, String


class AssessmentHistoryEntity(HistoryEntity):
    """
    评估历史
    """

    __tablename__ = "st_assessment_history"
    __table_args__ = {"comment": "评估历史"}
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


Index(
    "idx_assessment_history_time_range",
    AssessmentHistoryEntity.id,
    AssessmentHistoryEntity.commenced_on,
    AssessmentHistoryEntity.ceased_on.desc(),
    unique=True,
)

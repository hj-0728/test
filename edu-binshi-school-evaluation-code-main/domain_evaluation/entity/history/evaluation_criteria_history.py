from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String, Text, text


class EvaluationCriteriaHistoryEntity(HistoryEntity):
    """
    评价标准（历史实体类）
    """

    __tablename__ = "st_evaluation_criteria_history"
    __table_args__ = {"comment": "评价标准（历史）"}
    name = Column(String(255), comment="名称", nullable=False)
    status = Column(String(255), comment="状态", nullable=True)
    comments = Column(Text, comment="描述", nullable=True)
    evaluation_object_category = Column(String(255), comment="评价对象类型（学生、家长、老师等）", nullable=False)


Index(
    "idx_evaluation_criteria_history_time_range",
    EvaluationCriteriaHistoryEntity.id,
    EvaluationCriteriaHistoryEntity.begin_at,
    EvaluationCriteriaHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Text


class EvaluationCriteriaHistoryEntity(HistoryEntity):
    """
    评价标准历史
    """

    __tablename__ = "st_evaluation_criteria_history"
    __table_args__ = {"comment": "评价标准历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    status = Column(String(255), comment="状态（PUBLISHED/ARCHIVE/ABOLISHED）", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
    evaluation_object_category = Column(String(255), comment="评价对象类型（学生、家长、老师等）", nullable=False)
    period_id = Column(String(40), comment="周期id（每个学期都clone一下重新开始）", nullable=False)


Index(
    "idx_evaluation_criteria_history_time_range",
    EvaluationCriteriaHistoryEntity.id,
    EvaluationCriteriaHistoryEntity.commenced_on,
    EvaluationCriteriaHistoryEntity.ceased_on.desc(),
    unique=True,
)

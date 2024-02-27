from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, Integer, String, text


class EvaluationCriteriaTreeHistoryEntity(HistoryEntity):
    """
    评价标准（历史实体类）
    """

    __tablename__ = "st_evaluation_criteria_tree_history"
    __table_args__ = {"comment": "评价标准的树（对用户可以叫评价项）（历史）"}
    evaluation_criteria_id = Column(String(40), nullable=False, comment="评价标准id", index=True)
    parent_indicator_id = Column(String(40), nullable=True, comment="父级指标id")
    indicator_id = Column(String(40), nullable=False, comment="指标id")
    seq = Column(Integer, nullable=False, comment="排序码")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_evaluation_criteria_tree_history_time_range",
    EvaluationCriteriaTreeHistoryEntity.id,
    EvaluationCriteriaTreeHistoryEntity.begin_at,
    EvaluationCriteriaTreeHistoryEntity.end_at.desc(),
    unique=True,
)

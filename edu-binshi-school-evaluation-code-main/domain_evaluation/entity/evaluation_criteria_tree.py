from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, Integer, String, text

from domain_evaluation.entity.history.evaluation_criteria_tree_history import (
    EvaluationCriteriaTreeHistoryEntity,
)


class EvaluationCriteriaTreeEntity(VersionedEntity):
    __tablename__ = "st_evaluation_criteria_tree"
    __table_args__ = {"comment": "评价标准的树（对用户可以叫评价项）"}
    __history_entity__ = EvaluationCriteriaTreeHistoryEntity

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
    "idx_evaluation_criteria_tree_start_finish_time_range",
    EvaluationCriteriaTreeEntity.id,
    EvaluationCriteriaTreeEntity.start_at,
    EvaluationCriteriaTreeEntity.finish_at.desc(),
    unique=True,
)

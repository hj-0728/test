from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from domain_evaluation.entity.history.calc_score_input_history import CalcScoreInputHistoryEntity


class CalcScoreInputEntity(VersionedEntity):
    __tablename__ = "st_calc_score_input"
    __table_args__ = {"comment": "计算节点来源"}
    __history_entity__ = CalcScoreInputHistoryEntity

    calc_score_log_id = Column(String(40), nullable=False, comment="计划id", index=True)
    source_score_category = Column(String(255), nullable=False, comment="计算节点的类型")
    source_score_id = Column(String(40), nullable=False, comment="来源分数id")

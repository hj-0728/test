from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from domain_evaluation.entity.history.calc_score_log_history import CalcScoreLogHistoryEntity


class CalcScoreLogEntity(VersionedEntity):
    __tablename__ = "st_calc_score_log"
    __table_args__ = {"comment": "计算节点得分记录"}
    __history_entity__ = CalcScoreLogHistoryEntity

    evaluation_assignment_id = Column(String(40), nullable=False, comment="计划id", index=True)
    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)

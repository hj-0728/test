from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String

from domain_evaluation.entity.history.calc_score_output_history import CalcScoreOutputHistoryEntity


class CalcScoreOutputEntity(VersionedEntity):
    __tablename__ = "st_calc_score_output"
    __table_args__ = {"comment": "计算节点输出"}
    __history_entity__ = CalcScoreOutputHistoryEntity

    calc_score_log_id = Column(String(40), nullable=False, comment="计划id", index=True)
    numeric_score = Column(Numeric, nullable=True, comment="数字型的分数")
    string_score = Column(String(255), nullable=True, comment="字符串类型的分数")

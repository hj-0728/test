from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from domain_evaluation.entity.history.benchmark_calc_node_history import (
    BenchmarkCalcNodeHistoryEntity,
)


class BenchmarkCalcNodeEntity(VersionedEntity):
    __tablename__ = "st_benchmark_calc_node"
    __table_args__ = {"comment": "计算节点"}
    __history_entity__ = BenchmarkCalcNodeHistoryEntity

    benchmark_execute_node_id = Column(String(40), nullable=False, comment="节点id", index=True)
    input_score_symbol_id = Column(String(40), nullable=False, comment="输入的符号id")
    output_score_symbol_id = Column(String(40), nullable=False, comment="输出的符号id")
    calc_method = Column(String(255), nullable=False, comment="计算方法（统计类的、权重类的、区间取值的）")

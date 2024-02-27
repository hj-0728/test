from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, Numeric, String

from domain_evaluation.entity.history.benchmark_calc_node_weight_args_history import (
    BenchmarkCalcNodeWeightArgsHistoryEntity,
)


class BenchmarkCalcNodeWeightArgsEntity(VersionedEntity):
    __tablename__ = "st_benchmark_calc_node_weight_args"
    __table_args__ = {"comment": "计算方式为权重时的计算参数"}
    __history_entity__ = BenchmarkCalcNodeWeightArgsHistoryEntity

    benchmark_calc_node_id = Column(String(40), nullable=False, comment="计算节点的id", index=True)
    weight = Column(Numeric, nullable=False, comment="权重")
    seq = Column(Integer, nullable=False, comment="排序码")

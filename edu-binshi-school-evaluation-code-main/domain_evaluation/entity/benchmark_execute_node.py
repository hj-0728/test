from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String

from domain_evaluation.entity.history.benchmark_execute_node_history import (
    BenchmarkExecuteNodeHistoryEntity,
)


class BenchmarkExecuteNodeEntity(VersionedEntity):
    __tablename__ = "st_benchmark_execute_node"
    __table_args__ = {"comment": "基准的执行节点"}
    __history_entity__ = BenchmarkExecuteNodeHistoryEntity

    benchmark_id = Column(String(40), nullable=False, comment="基准id", index=True)
    name = Column(String(255), nullable=False, comment="名称")
    category = Column(String(255), nullable=False, comment="类型（input、calc）")
    next_node_id = Column(String(40), nullable=True, comment="下一节点id")
    seq = Column(Integer, nullable=False, comment="排序码")

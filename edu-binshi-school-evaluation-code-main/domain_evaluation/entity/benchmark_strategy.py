from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String, text

from domain_evaluation.entity.history.benchmark_strategy_history import (
    BenchmarkStrategyHistoryEntity,
)


class BenchmarkStrategyEntity(VersionedEntity):
    """
    基准的策略
    """

    __tablename__ = "st_benchmark_strategy"
    __table_args__ = {"comment": "基准的策略"}
    __history_entity__ = BenchmarkStrategyHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="名称", nullable=False)
    process_params_type = Column(
        String(255), comment="输入参数的类型（一个策略一个model，方便转json）", nullable=False
    )
    prepare_func = Column(String(255), comment="准备input_params_type的方法", nullable=False)
    build_node_func = Column(String(255), comment="创建节点的函数", nullable=False)
    score_symbol_scope = Column(String(255), comment="得分符号的范围", nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )
    source_category = Column(String(255), comment="input/calc", nullable=False)


Index(
    "idx_benchmark_strategy_start_finish_time_range",
    BenchmarkStrategyEntity.id,
    BenchmarkStrategyEntity.start_at,
    BenchmarkStrategyEntity.finish_at.desc(),
    unique=True,
)

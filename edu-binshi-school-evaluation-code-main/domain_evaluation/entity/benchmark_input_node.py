from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import ARRAY, Column, DateTime, Index, Numeric, String, text
from sqlalchemy.dialects.postgresql import JSONB

from domain_evaluation.entity.history.benchmark_input_node_history import (
    BenchmarkInputNodeHistoryEntity,
)


class BenchmarkInputNodeEntity(VersionedEntity):
    __tablename__ = "st_benchmark_input_node"
    __table_args__ = {"comment": "输入节点"}
    __history_entity__ = BenchmarkInputNodeHistoryEntity

    benchmark_execute_node_id = Column(String(40), nullable=False, comment="节点id", index=True)
    source_category = Column(String(255), nullable=False, comment="来源种类（input、benchmark）")
    source_benchmark_id = Column(String(40), nullable=True, comment="引用的benchmark_id")
    source_exec_mode = Column(String(255), nullable=True, comment="freedom/once/scheduler")
    scheduler_expression = Column(String(255), nullable=True, comment="scheduler表达式，cron格式的")
    filler_calc_method = Column(String(255), nullable=True, comment="根据category去调用对应的填写者计算的类")
    filler_calc_context = Column(JSONB, nullable=True, comment="填写者计算的上下文")
    score_symbol_id = Column(String(40), nullable=False, comment="符号id")
    numeric_min_score = Column(Numeric, nullable=True, comment="最小值")
    numeric_max_score = Column(Numeric, nullable=True, comment="最大值")
    limited_string_options = Column(ARRAY(String(255)), nullable=True, comment="字符串的选项")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_benchmark_input_node_start_finish_time_range",
    BenchmarkInputNodeEntity.id,
    BenchmarkInputNodeEntity.start_at,
    BenchmarkInputNodeEntity.finish_at.desc(),
    unique=True,
)

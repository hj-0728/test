from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import JSONB


class BenchmarkHistoryEntity(HistoryEntity):
    """
    基准（历史实体类）
    """

    __tablename__ = "st_benchmark_history"
    __table_args__ = {"comment": "基准（历史）"}
    indicator_id = Column(String(40), comment="评价指标id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    guidance = Column(String(500), comment="指南", nullable=True)
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始时间")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束时间（默认infinity，如果被删加上时间）",
        server_default=text("'infinity'::timestamptz"),
    )
    benchmark_strategy_id = Column(
        String(40), comment="基准策略id(给页面参考的需要填写的东西)", nullable=False, index=True
    )
    benchmark_strategy_params = Column(JSONB, comment="页面输入的内容", nullable=True)


Index(
    "idx_benchmark_history_time_range",
    BenchmarkHistoryEntity.id,
    BenchmarkHistoryEntity.begin_at,
    BenchmarkHistoryEntity.end_at.desc(),
    unique=True,
)

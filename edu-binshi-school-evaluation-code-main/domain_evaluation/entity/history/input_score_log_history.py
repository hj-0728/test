from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, Numeric, String


class InputScoreLogHistoryEntity(HistoryEntity):
    __tablename__ = "st_input_score_log_history"
    __table_args__ = {"comment": "输入分数的日志（历史）"}

    evaluation_assignment_id = Column(String(40), nullable=False, comment="计划id", index=True)
    benchmark_input_node_id = Column(String(40), nullable=False, comment="输入节点的id", index=True)
    generated_at = Column(DateTime(timezone=True), nullable=False, comment="生成时间")
    expected_filler_category = Column(String(255), nullable=False, comment="期望填写的资源类型")
    expected_filler_id = Column(String(40), nullable=False, comment="期望填写的资源id")
    filler_category = Column(String(255), nullable=True, comment="填写的资源类型")
    filler_id = Column(String(40), nullable=True, comment="填写的资源id")
    fill_start_at = Column(DateTime(timezone=True), nullable=False, comment="填写开始时间")
    fill_finish_at = Column(DateTime(timezone=True), nullable=False, comment="填写结束时间")
    filled_at = Column(DateTime(timezone=True), nullable=True, comment="填写时间")
    numeric_score = Column(Numeric, nullable=True, comment="数字型的分数")
    string_score = Column(String(255), nullable=True, comment="字符串类型的分数")
    status = Column(String(255), nullable=False, comment="状态")
    comments = Column(String(500), nullable=True, comment="描述")


Index(
    "idx_input_score_log_history_time_range",
    InputScoreLogHistoryEntity.id,
    InputScoreLogHistoryEntity.begin_at,
    InputScoreLogHistoryEntity.end_at.desc(),
    unique=True,
)

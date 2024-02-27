from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class MedalIssuedLogHistoryEntity(HistoryEntity):
    """
    勋章发放日志历史
    """

    __tablename__ = "st_medal_issued_log_history"
    __table_args__ = {"comment": "勋章发放日志历史"}
    medal_id = Column(String(40), comment="勋章id", nullable=False)
    calc_rule_id = Column(String(40), comment="计算规则id", nullable=False)
    issued_res_category = Column(
        String(255), comment="发放资源类别（DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）", nullable=False
    )
    issued_res_id = Column(String(40), comment="发放资源id", nullable=False)
    issued_on = Column(DateTime(timezone=True), comment="发放时间", nullable=False)
    status = Column(String(255), comment="状态（ISSUED/REVOKED）", nullable=False)


Index(
    "idx_medal_issued_log_history_time_range",
    MedalIssuedLogHistoryEntity.id,
    MedalIssuedLogHistoryEntity.commenced_on,
    MedalIssuedLogHistoryEntity.ceased_on.desc(),
    unique=True,
)

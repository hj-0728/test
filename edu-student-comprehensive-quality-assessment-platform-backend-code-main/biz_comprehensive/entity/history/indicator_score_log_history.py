from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Numeric, String


class IndicatorScoreLogHistoryEntity(HistoryEntity):
    """
    指标得分日志历史
    """

    __tablename__ = "st_indicator_score_log_history"
    __table_args__ = {"comment": "指标得分日志历史"}
    indicator_score_id = Column(String(40), comment="指标得分id", nullable=False)
    owner_res_category = Column(
        String(255),
        comment="所属资源类别（部门/学生 DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）",
        nullable=False,
    )
    owner_res_id = Column(String(40), comment="所属资源id", nullable=False)
    string_score = Column(String(255), comment="字符串得分", nullable=False)
    numeric_score = Column(Numeric, comment="数值得分", nullable=False)


Index(
    "idx_indicator_score_log_history_time_range",
    IndicatorScoreLogHistoryEntity.id,
    IndicatorScoreLogHistoryEntity.commenced_on,
    IndicatorScoreLogHistoryEntity.ceased_on.desc(),
    unique=True,
)

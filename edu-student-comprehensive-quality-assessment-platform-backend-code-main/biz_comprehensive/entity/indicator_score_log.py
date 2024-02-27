from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String

from biz_comprehensive.entity.history.indicator_score_log_history import (
    IndicatorScoreLogHistoryEntity,
)


class IndicatorScoreLogEntity(VersionedEntity):
    """
    指标得分日志
    """

    __tablename__ = "st_indicator_score_log"
    __table_args__ = {"comment": "指标得分日志"}
    __history_entity__ = IndicatorScoreLogHistoryEntity
    indicator_score_id = Column(String(40), comment="指标得分id", nullable=False)
    owner_res_category = Column(
        String(255),
        comment="所属资源类别（部门/学生 DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）",
        nullable=False,
    )
    owner_res_id = Column(String(40), comment="所属资源id", nullable=False)
    string_score = Column(String(255), comment="字符串得分", nullable=False)
    numeric_score = Column(Numeric, comment="数值得分", nullable=False)

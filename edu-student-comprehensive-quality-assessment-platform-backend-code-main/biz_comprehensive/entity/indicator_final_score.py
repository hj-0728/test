from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String

from biz_comprehensive.entity.history.indicator_final_score_history import (
    IndicatorFinalScoreHistoryEntity,
)


class IndicatorFinalScoreEntity(VersionedEntity):
    """
    指标最终得分
    """

    __tablename__ = "st_indicator_final_score"
    __table_args__ = {"comment": "指标最终得分"}
    __history_entity__ = IndicatorFinalScoreHistoryEntity
    owner_res_category = Column(
        String(255),
        comment="所属资源类别（部门/学生,DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）",
        nullable=False,
    )
    owner_res_id = Column(String(40), comment="所属资源id", nullable=False)
    indicator_id = Column(String(40), comment="指标id", nullable=False)
    numeric_score = Column(Numeric, comment="数值得分", nullable=False)
    string_score = Column(String(255), comment="字符串得分", nullable=False)

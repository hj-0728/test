from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Numeric, String, Text

from biz_comprehensive.entity.history.assessment_result_history import AssessmentResultHistoryEntity


class AssessmentResultEntity(VersionedEntity):
    """
    评估结果
    """

    __tablename__ = "st_assessment_result"
    __table_args__ = {"comment": "评估结果"}
    __history_entity__ = AssessmentResultHistoryEntity
    assessment_id = Column(String(40), comment="评估id", nullable=False)
    establishment_assign_id = Column(String(40), comment="编制分配id", nullable=False)
    result_string_value = Column(String(255), comment="结果字符串值", nullable=True)
    result_numeric_value = Column(Numeric, comment="结果数值值", nullable=True)
    status = Column(String(255), comment="状态（Absent/Invalidated/Confirmed）", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)

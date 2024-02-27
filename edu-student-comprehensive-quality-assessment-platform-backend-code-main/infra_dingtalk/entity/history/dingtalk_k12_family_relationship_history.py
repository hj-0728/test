"""
学生家长关系历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DingtalkK12FamilyRelationshipHistoryEntity(HistoryEntity):
    """
    k12学生历史表
    """

    __tablename__ = "st_dingtalk_k12_family_relationship_history"
    __table_args__ = {"comment": "学生家长关系历史表"}
    dingtalk_k12_student_id = Column(String(40), comment="学生id", nullable=False, index=True)
    dingtalk_k12_parent_id = Column(String(40), comment="家长id", nullable=False, index=True)
    relationship_code = Column(String(255), comment="关系code", nullable=False)
    relationship_name = Column(String(255), comment="关系名称", nullable=False)


# 时间检索索引
Index(
    "idx_dingtalk_k12_family_relationship_history_time_range",
    DingtalkK12FamilyRelationshipHistoryEntity.id,
    DingtalkK12FamilyRelationshipHistoryEntity.commenced_on,
    DingtalkK12FamilyRelationshipHistoryEntity.ceased_on.desc(),
    unique=True,
)

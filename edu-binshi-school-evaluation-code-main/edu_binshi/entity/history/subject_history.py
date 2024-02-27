"""
科目历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, text


class SubjectHistoryEntity(HistoryEntity):
    """
    科目（历史实体类）
    """

    __tablename__ = "st_subject_history"
    __table_args__ = {"comment": "科目（历史）"}
    name = Column(String(255), comment="名称", nullable=False)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))


Index(
    "idx_subject_history_time_range",
    SubjectHistoryEntity.id,
    SubjectHistoryEntity.begin_at,
    SubjectHistoryEntity.end_at.desc(),
    unique=True,
)

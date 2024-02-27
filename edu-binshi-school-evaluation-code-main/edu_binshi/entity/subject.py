"""
科目实体类
"""
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from edu_binshi.entity.history.subject_history import SubjectHistoryEntity


class SubjectEntity(VersionedEntity):
    """
    科目
    """

    __tablename__ = "st_subject"
    __table_args__ = {"comment": "科目"}
    __history_entity__ = SubjectHistoryEntity
    name = Column(String(255), comment="名称", nullable=False, unique=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.subject_history import SubjectHistoryEntity


class SubjectEntity(VersionedEntity):
    """
    科目
    """

    __tablename__ = "st_subject"
    __table_args__ = {"comment": "科目"}
    __history_entity__ = SubjectHistoryEntity
    name = Column(String(255), comment="科目名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class SubjectHistoryEntity(HistoryEntity):
    """
    科目历史
    """

    __tablename__ = "st_subject_history"
    __table_args__ = {"comment": "科目历史"}
    name = Column(String(255), comment="科目名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)


Index(
    "idx_subject_history_time_range",
    SubjectHistoryEntity.id,
    SubjectHistoryEntity.commenced_on,
    SubjectHistoryEntity.ceased_on.desc(),
    unique=True,
)

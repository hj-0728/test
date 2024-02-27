from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class PeopleRelationshipHistoryEntity(HistoryEntity):
    """
    人员关系历史
    """

    __tablename__ = "st_people_relationship_history"
    __table_args__ = {"comment": "人员关系历史"}

    subject_people_id = Column(String(40), nullable=False, comment="人员id", index=True)
    object_people_id = Column(String(40), nullable=False, comment="关系人员id", index=True)
    relationship = Column(String(255), nullable=False, comment="关系", index=True)
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_people_relationship_history_time_range",
    PeopleRelationshipHistoryEntity.id,
    PeopleRelationshipHistoryEntity.begin_at,
    PeopleRelationshipHistoryEntity.end_at.desc(),
    unique=True,
)

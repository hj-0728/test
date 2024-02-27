from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, String, text

from infra_backbone.entity.history.people_relationship_history import (
    PeopleRelationshipHistoryEntity,
)


class PeopleRelationshipEntity(VersionedEntity):
    """
    人员关系
    """

    __tablename__ = "st_people_relationship"
    __table_args__ = {"comment": "人员关系"}
    __history_entity__ = PeopleRelationshipHistoryEntity

    subject_people_id = Column(String(40), nullable=False, comment="人员id", index=True)
    object_people_id = Column(String(40), nullable=False, comment="关系人员id", index=True)
    relationship = Column(String(255), nullable=False, comment="关系", index=True)
    started_on = Column(DateTime(timezone=True), nullable=False, comment="开始于")
    ended_on = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )

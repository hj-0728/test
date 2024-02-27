from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Integer, String, text

from infra_backbone.entity.history.establishment_assign_history import (
    EstablishmentAssignHistoryEntity,
)


class EstablishmentAssignEntity(VersionedEntity):
    """
    编制分配
    """

    __tablename__ = "st_establishment_assign"
    __table_args__ = {"comment": "编制分配"}
    __history_entity__ = EstablishmentAssignHistoryEntity

    establishment_id = Column(String(40), nullable=False, comment="维度部门树id", index=True)
    people_id = Column(String(40), nullable=False, comment="People Id", index=True)
    comments = Column(String(255), nullable=True, comment="描述")
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"))
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )

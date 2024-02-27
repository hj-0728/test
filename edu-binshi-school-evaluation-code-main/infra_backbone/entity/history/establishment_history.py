from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, Integer, String, text


class EstablishmentHistoryEntity(HistoryEntity):
    """
    编制历史
    """

    __tablename__ = "st_establishment_history"
    __table_args__ = {"comment": "编制历史"}

    dimension_dept_tree_id = Column(String(40), nullable=False, comment="维度部门树id", index=True)
    capacity_id = Column(String(40), nullable=False, comment="Capacity Id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"), index=True)
    comments = Column(String(255), nullable=True, comment="描述")
    start_at = Column(DateTime(timezone=True), nullable=True, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_establishment_history_time_range",
    EstablishmentHistoryEntity.id,
    EstablishmentHistoryEntity.begin_at,
    EstablishmentHistoryEntity.end_at.desc(),
    unique=True,
)

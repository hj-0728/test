from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, text


class EstablishmentAssignHistoryEntity(HistoryEntity):
    """
    编制分配历史
    """

    __tablename__ = "st_establishment_assign_history"
    __table_args__ = {"comment": "编制分配历史"}

    establishment_id = Column(String(40), nullable=False, comment="维度部门树id", index=True)
    people_id = Column(String(40), nullable=False, comment="People Id", index=True)
    comments = Column(String(255), nullable=True, comment="描述")
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"))


Index(
    "idx_establishment_assign_history_time_range",
    EstablishmentAssignHistoryEntity.id,
    EstablishmentAssignHistoryEntity.commenced_on,
    EstablishmentAssignHistoryEntity.ceased_on.desc(),
    unique=True,
)

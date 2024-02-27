from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, text

from infra_backbone.entity.history.establishment_history import EstablishmentHistoryEntity


class EstablishmentEntity(VersionedEntity):
    """
    编制，维度树上与capacity的组合
    """

    __tablename__ = "st_establishment"
    __table_args__ = {"comment": "编制"}
    __history_entity__ = EstablishmentHistoryEntity

    dimension_dept_tree_id = Column(String(40), nullable=False, comment="维度部门树id", index=True)
    capacity_id = Column(String(40), nullable=False, comment="Capacity Id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"), index=True)
    comments = Column(String(255), nullable=True, comment="描述")

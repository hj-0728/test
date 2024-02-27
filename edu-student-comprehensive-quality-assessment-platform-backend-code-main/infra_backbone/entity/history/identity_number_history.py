"""
身份编号  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class IdentityNumberHistoryEntity(HistoryEntity):
    """
    身份编号 历史实体类
    """

    __tablename__ = "st_identity_number_history"
    __table_args__ = {"comment": "身份编号"}

    owner_id = Column(String(40), nullable=False, comment="拥有者id")
    owner_category = Column(String(255), nullable=False, comment="拥有者类型")
    category = Column(String(255), nullable=False, comment="类型", index=True)
    number = Column(String(255), nullable=False, comment="编号")


Index(
    "idx_identity_number_history_time_range",
    IdentityNumberHistoryEntity.id,
    IdentityNumberHistoryEntity.commenced_on,
    IdentityNumberHistoryEntity.ceased_on.desc(),
    unique=True,
)


Index(
    "idx_identity_number_history_resource_info",
    IdentityNumberHistoryEntity.owner_category,
    IdentityNumberHistoryEntity.owner_id,
)

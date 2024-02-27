"""
维度  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DimensionHistoryEntity(HistoryEntity):
    """
    维度  历史实体类
    """

    __tablename__ = "st_dimension_history"
    __table_args__ = {"comment": "维度"}

    organization_id = Column(String(40), nullable=False, comment="组织id")
    name = Column(String(255), nullable=False, comment="维度名称")
    code = Column(String(255), nullable=False, comment="维度编码")
    category = Column(String(255), nullable=False, comment="类别，用枚举处理")


Index(
    "idx_dimension_history_time_range",
    DimensionHistoryEntity.id,
    DimensionHistoryEntity.commenced_on,
    DimensionHistoryEntity.ceased_on.desc(),
    unique=True,
)

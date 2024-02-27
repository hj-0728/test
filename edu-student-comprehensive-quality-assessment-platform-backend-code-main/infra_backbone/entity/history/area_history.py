"""
地域  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AreaHistoryEntity(HistoryEntity):
    """
    地域  历史实体类
    """

    __tablename__ = "st_area_history"
    __table_args__ = {"comment": "地域"}

    parent_id = Column(String(40), nullable=True, comment="父id，空的为根节点")
    name = Column(String(255), nullable=False, comment="名称")
    zoning_code = Column(String(255), nullable=True, comment="行政区划代码")


Index(
    "idx_area_history_time_range",
    AreaHistoryEntity.id,
    AreaHistoryEntity.commenced_on,
    AreaHistoryEntity.ceased_on.desc(),
    unique=True,
)

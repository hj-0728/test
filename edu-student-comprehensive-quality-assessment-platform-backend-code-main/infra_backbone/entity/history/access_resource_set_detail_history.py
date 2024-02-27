"""
访问资源集合详情  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String


class AccessResourceSetDetailHistoryEntity(HistoryEntity):
    """
    访问资源集合详情  历史实体类
    """

    __tablename__ = "st_access_resource_set_detail_history"
    __table_args__ = {"comment": "访问资源集合详情"}

    access_resource_set_id = Column(String(40), nullable=False, comment="前端路径id")
    bind_resource_category = Column(String(40), nullable=True, comment="资源类别")
    bind_resource_id = Column(Integer, nullable=True, comment="资源id")


Index(
    "idx_access_resource_set_detail_history_time_range",
    AccessResourceSetDetailHistoryEntity.id,
    AccessResourceSetDetailHistoryEntity.commenced_on,
    AccessResourceSetDetailHistoryEntity.ceased_on.desc(),
    unique=True,
)

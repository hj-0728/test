"""
路由验证方式 历史实体类
"""

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class RoutePermitHistoryEntity(HistoryEntity):
    """
    路由验证方式
    """

    __tablename__ = "st_route_permit_history"
    __table_args__ = {"comment": "路由验证方式"}
    route_id = Column(String(40), comment="路由id", nullable=False, index=True)
    permitted_resource_category = Column(String(255), comment="许可资源类型", nullable=False)
    permitted_resource_id = Column(String(255), comment="许可资源id", nullable=False)


Index(
    "idx_route_permit_history_time_range",
    RoutePermitHistoryEntity.id,
    RoutePermitHistoryEntity.begin_at,
    RoutePermitHistoryEntity.end_at.desc(),
    unique=True,
)

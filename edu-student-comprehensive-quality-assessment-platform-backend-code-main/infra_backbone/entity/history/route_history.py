from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class RouteHistoryEntity(HistoryEntity):
    """
    路由信息历史
    """

    __tablename__ = "st_route_history"
    __table_args__ = {"comment": "路由信息历史"}

    category = Column(String(255), nullable=False, comment="frontend/backend", index=True)
    path = Column(String(255), nullable=False, comment="路径")
    entry_code = Column(String(255), comment="编码")
    access_strategy = Column(
        String(255), nullable=False, comment="访问策略枚举，ignore/authorized/controlled"
    )


Index(
    "idx_route_history_time_range",
    RouteHistoryEntity.id,
    RouteHistoryEntity.commenced_on,
    RouteHistoryEntity.ceased_on.desc(),
    unique=True,
)

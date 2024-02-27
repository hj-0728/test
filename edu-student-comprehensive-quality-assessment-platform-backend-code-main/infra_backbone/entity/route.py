from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, UniqueConstraint

from infra_backbone.entity.history.route_history import RouteHistoryEntity


class RouteEntity(VersionedEntity):
    """
    路由信息
    """

    __tablename__ = "st_route"
    __table_args__ = (
        UniqueConstraint("category", "path", name="uc_route_category_path"),
        {"comment": "路由信息"},
    )
    __history_entity__ = RouteHistoryEntity
    category = Column(String(255), nullable=False, comment="frontend/backend", index=True)
    path = Column(String(255), nullable=False, comment="路径")
    entry_code = Column(String(255), comment="编码")
    access_strategy = Column(
        String(255), nullable=False, comment="访问策略枚举，ignore/authorized/controlled"
    )

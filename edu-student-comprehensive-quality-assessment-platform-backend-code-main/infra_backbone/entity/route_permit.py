from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.route_permit_history import RoutePermitHistoryEntity


class RoutePermitEntity(VersionedEntity):
    """
    路由验证方式
    """

    __tablename__ = "st_route_permit"
    __table_args__ = {"comment": "路由验证方式"}
    __history_entity__ = RoutePermitHistoryEntity

    route_id = Column(String(40), comment="路由id", nullable=False, index=True)
    permitted_resource_category = Column(String(255), comment="许可资源类型", nullable=False)
    permitted_resource_id = Column(String(255), comment="许可资源id", nullable=False)


Index(
    "idx_route_permit_permitted_resource",
    RoutePermitEntity.permitted_resource_category,
    RoutePermitEntity.permitted_resource_id,
)

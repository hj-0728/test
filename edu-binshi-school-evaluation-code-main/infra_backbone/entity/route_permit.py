from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

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

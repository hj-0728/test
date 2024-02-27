from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String, text

from infra_backbone.entity.history.data_permission_detail_history import (
    DataPermissionDetailHistoryEntity,
)


class DataPermissionDetailEntity(VersionedEntity):
    """
    数据权限详情
    """

    __tablename__ = "st_data_permission_detail"
    __table_args__ = {"comment": "数据权限详情"}
    __history_entity__ = DataPermissionDetailHistoryEntity

    data_permission_id = Column(String(40), nullable=False, comment="数据权限id", index=True)
    object_id = Column(String(40), nullable=False, comment="对象id")
    object_category = Column(String(255), nullable=False, comment="对象类型")
    start_at = Column(DateTime(timezone=True), nullable=False, comment="开始于")
    finish_at = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="结束于",
        server_default=text("'infinity'::timestamptz"),
    )


Index(
    "idx_data_permission_detail_resource_info",
    DataPermissionDetailEntity.object_category,
    DataPermissionDetailEntity.object_id,
)

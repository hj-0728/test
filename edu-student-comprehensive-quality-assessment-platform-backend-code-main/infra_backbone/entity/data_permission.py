from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Index, String

from infra_backbone.entity.history.data_permission_history import DataPermissionHistoryEntity


class DataPermissionEntity(VersionedEntity):
    """
    数据权限
    """

    __tablename__ = "st_data_permission"
    __table_args__ = {"comment": "数据权限"}
    __history_entity__ = DataPermissionHistoryEntity

    subject_category = Column(String(255), nullable=False, comment="主资源类别")
    subject_id = Column(String(40), nullable=False, comment="主资源id")
    aspect = Column(String(255), nullable=False, comment="轴", index=True)
    policy = Column(String(255), nullable=False, comment="策略:允许/拒绝", index=True)


Index(
    "idx_data_permission_resource_info",
    DataPermissionEntity.subject_category,
    DataPermissionEntity.subject_id,
)

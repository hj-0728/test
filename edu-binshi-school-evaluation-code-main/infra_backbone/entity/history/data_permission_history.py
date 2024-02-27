from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class DataPermissionHistoryEntity(HistoryEntity):
    """
    数据权限历史
    """

    __tablename__ = "st_data_permission_history"
    __table_args__ = {"comment": "数据权限历史"}

    subject_category = Column(String(255), nullable=False, comment="主资源类别")
    subject_id = Column(String(40), nullable=False, comment="主资源id")
    aspect = Column(String(255), nullable=False, comment="轴", index=True)
    policy = Column(String(255), nullable=False, comment="策略:允许/拒绝", index=True)


Index(
    "idx_data_permission_history_time_range",
    DataPermissionHistoryEntity.id,
    DataPermissionHistoryEntity.begin_at,
    DataPermissionHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String, text


class DataPermissionDetailHistoryEntity(HistoryEntity):
    """
    数据权限细节历史
    """

    __tablename__ = "st_data_permission_detail_history"
    __table_args__ = {"comment": "数据权限细节历史"}

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
    "idx_data_permission_detail_history_time_range",
    DataPermissionDetailHistoryEntity.id,
    DataPermissionDetailHistoryEntity.begin_at,
    DataPermissionDetailHistoryEntity.end_at.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AccessResourceSetHistoryEntity(HistoryEntity):
    """
    访问资源集合历史
    """

    __tablename__ = "st_access_resource_set_history"
    __table_args__ = {"comment": "访问资源集合历史"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")


Index(
    "idx_access_resource_set_history_time_range",
    AccessResourceSetHistoryEntity.id,
    AccessResourceSetHistoryEntity.begin_at,
    AccessResourceSetHistoryEntity.end_at.desc(),
    unique=True,
)

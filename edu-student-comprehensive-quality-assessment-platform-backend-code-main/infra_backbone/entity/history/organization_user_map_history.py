from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class OrganizationUserMapHistoryEntity(HistoryEntity):
    """
    组织用户map 历史
    """

    __tablename__ = "st_organization_user_map_history"
    __table_args__ = {"comment": "组织用户map 历史"}

    organization_id = Column(String(40), nullable=False, comment="组织id", index=True)
    user_id = Column(String(40), nullable=False, comment="用户id", index=True)


Index(
    "idx_organization_user_map_history_time_range",
    OrganizationUserMapHistoryEntity.id,
    OrganizationUserMapHistoryEntity.commenced_on,
    OrganizationUserMapHistoryEntity.ceased_on.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ContextOrganizationCorpMapHistoryEntity(HistoryEntity):
    """
    上下文组织关联（历史实体类）
    """

    __tablename__ = "st_context_organization_corp_map_history"
    __table_args__ = {"comment": "上下文组织关联（历史）"}
    organization_id = Column(String(40), comment="组织id", nullable=False)
    res_category = Column(String(255), comment="关联corp类型", nullable=False)
    res_id = Column(String(40), comment="关联corpid", nullable=True)


Index(
    "idx_context_organization_corp_map_history_time_range",
    ContextOrganizationCorpMapHistoryEntity.id,
    ContextOrganizationCorpMapHistoryEntity.commenced_on,
    ContextOrganizationCorpMapHistoryEntity.ceased_on.desc(),
    unique=True,
)

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ContactInfoHistoryEntity(HistoryEntity):
    """
    联系方式历史
    """

    __tablename__ = "st_contact_info_history"
    __table_args__ = {"comment": "联系方式历史"}

    category = Column(String(255), nullable=False, index=True, comment="联系方式类别")
    detail = Column(String(255), nullable=False, comment="联系方式详情")


Index(
    "idx_contact_info_history_time_range",
    ContactInfoHistoryEntity.id,
    ContactInfoHistoryEntity.commenced_on,
    ContactInfoHistoryEntity.ceased_on.desc(),
    unique=True,
)

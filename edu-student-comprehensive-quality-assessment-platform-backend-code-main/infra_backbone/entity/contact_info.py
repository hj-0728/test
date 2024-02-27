from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.contact_info_history import ContactInfoHistoryEntity


class ContactInfoEntity(VersionedEntity):
    """
    联系方式
    """

    __tablename__ = "st_contact_info"
    __table_args__ = {"comment": "联系方式"}
    __history_entity__ = ContactInfoHistoryEntity

    category = Column(String(255), nullable=False, index=True, comment="联系方式类别")
    detail = Column(String(255), nullable=False, comment="联系方式详情")

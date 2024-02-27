from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from infra_backbone.entity.history.file_public_link_history import FilePublicLinkHistoryEntity


class FilePublicLinkEntity(VersionedEntity):
    """
    文件的公开连接
    """

    __tablename__ = "st_file_public_link"
    __table_args__ = {"comment": "文件的公开连接"}
    __history_entity__ = FilePublicLinkHistoryEntity

    file_id = Column(String(40), nullable=False, comment="文件id", index=True)
    public_link = Column(Text, nullable=False, comment="公开链接")

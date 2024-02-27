from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Text


class FilePublicLinkHistoryEntity(HistoryEntity):
    """
    文件的公开连接历史
    """

    __tablename__ = "st_file_public_link_history"
    __table_args__ = {"comment": "文件的公开连接历史"}

    file_id = Column(String(40), nullable=False, comment="文件id", index=True)
    public_link = Column(Text, nullable=False, comment="公开链接")


Index(
    "idx_file_public_link_history_time_range",
    FilePublicLinkHistoryEntity.id,
    FilePublicLinkHistoryEntity.commenced_on,
    FilePublicLinkHistoryEntity.ceased_on.desc(),
    unique=True,
)

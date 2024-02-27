from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, String


class TagInfoHistoryEntity(HistoryEntity):
    """
    标签历史
    """

    __tablename__ = "st_tag_info_history"
    __table_args__ = {"comment": "标签历史"}

    name = Column(String(255), nullable=False, comment="名称")

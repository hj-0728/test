"""
用户配置  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Text


class UserConfigHistoryEntity(HistoryEntity):
    """
    用户配置历史
    """

    __tablename__ = "st_user_config_history"
    __table_args__ = {"comment": "用户配置历史"}

    user_id = Column(String(40), nullable=False, comment="用户id", index=True)
    config_key = Column(String(255), nullable=False, comment="key", index=True)
    config_value = Column(Text, nullable=True, comment="值")


Index(
    "idx_user_config_history_time_range",
    UserConfigHistoryEntity.id,
    UserConfigHistoryEntity.commenced_on,
    UserConfigHistoryEntity.ceased_on.desc(),
    unique=True,
)

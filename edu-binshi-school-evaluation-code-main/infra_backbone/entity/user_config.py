from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from infra_backbone.entity.history.user_config_history import UserConfigHistoryEntity


class UserConfigEntity(VersionedEntity):
    """
    用户配置
    """

    __tablename__ = "st_user_config"
    __table_args__ = {"comment": "用户配置"}
    __history_entity__ = UserConfigHistoryEntity

    user_id = Column(String(40), nullable=False, comment="用户id", index=True)
    config_key = Column(String(255), nullable=False, comment="key", index=True)
    config_value = Column(Text, nullable=True, comment="值")

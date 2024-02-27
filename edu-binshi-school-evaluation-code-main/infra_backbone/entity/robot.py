from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.robot_history import RobotHistoryEntity


class RobotEntity(VersionedEntity):
    """
    机器人  实体类
    """

    __tablename__ = "st_robot"
    __table_args__ = {"comment": "机器人"}
    __history_entity__ = RobotHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
    access_key = Column(String(255), nullable=False, comment="访问key")
    secret_key = Column(String(255), nullable=False, comment="安全key")
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))

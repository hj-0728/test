"""
机器人  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, text


class RobotHistoryEntity(HistoryEntity):
    """
    机器人  历史实体类
    """

    __tablename__ = "st_robot_history"
    __table_args__ = {"comment": "机器人"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码", index=True)
    access_key = Column(String(255), nullable=False, comment="访问key")
    secret_key = Column(String(255), nullable=False, comment="安全key")
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))


Index(
    "idx_robot_history_time_range",
    RobotHistoryEntity.id,
    RobotHistoryEntity.commenced_on,
    RobotHistoryEntity.ceased_on.desc(),
    unique=True,
)

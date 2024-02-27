from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text

from infra_backbone.entity.history.user_history import UserHistoryEntity


class UserEntity(VersionedEntity):
    """
    用户
    """

    __tablename__ = "st_user"
    __table_args__ = {"comment": "用户"}
    __history_entity__ = UserHistoryEntity

    name = Column(String(255), nullable=False, comment="姓名", index=True, unique=True)
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))
    valid_until = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="有效期至",
        server_default=text("'infinity'::timestamptz"),
    )
    password = Column(String(255), nullable=False, comment="密码")
    salt = Column(String(255), nullable=False, comment="盐")
    try_count = Column(Integer, nullable=False, comment="尝试次数", server_default=text("0"))
    password_reset = Column(
        Boolean, nullable=False, comment="用户登录时是否需要重置密码", server_default=text("true")
    )

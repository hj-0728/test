from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, text


class UserHistoryEntity(HistoryEntity):
    """
    用户历史
    """

    __tablename__ = "st_user_history"
    __table_args__ = {"comment": "用户历史"}

    name = Column(String(255), nullable=False, comment="姓名", index=True)
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


Index(
    "idx_user_history_time_range",
    UserHistoryEntity.id,
    UserHistoryEntity.begin_at,
    UserHistoryEntity.end_at.desc(),
    unique=True,
)

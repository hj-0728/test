"""
钉钉用户
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, DateTime, JSON, String, UniqueConstraint

from infra_dingtalk.entity.history.dingtalk_user_history import DingtalkUserHistoryEntity


class DingtalkUserEntity(VersionedEntity):
    """
    钉钉用户
    """

    __tablename__ = "st_dingtalk_user"
    __table_args__ = (
        UniqueConstraint(
            "remote_user_id",
            "dingtalk_corp_id",
            name="st_dingtalk_user_remote_user_id_dingtalk_corp_id_key",
        ),
        {"comment": "钉钉用户"},
    )
    __history_entity__ = DingtalkUserHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_user_id = Column(String(255), comment="远程用户id", nullable=False)
    unionid = Column(String(255), comment="远程用户unionid", nullable=False)
    name = Column(String(255), comment="用户名", nullable=False)
    avatar = Column(String(255), comment="头像")
    state_code = Column(String(255), comment="国际电话区号")
    mobile = Column(String(255), comment="手机号码")
    hide_mobile = Column(Boolean, nullable=False, comment="是否隐藏号码")
    telephone = Column(String(255), comment="分机号")
    job_number = Column(String(255), comment="员工工号")
    email = Column(String(255), comment="邮箱")
    org_mail = Column(String(255), comment="员工企业邮箱")
    work_place = Column(String(255), comment="办公地点")
    extension = Column(JSON, comment="其他属性")
    hired_date = Column(DateTime(timezone=True), comment="入职时间")
    admin = Column(Boolean, nullable=False, comment="是否为企业管理员")
    boss = Column(Boolean, nullable=False, comment="是否为企业老板")
    exclusive_account = Column(Boolean, comment="是否专属账号")

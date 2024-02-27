"""
k12学生历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, JSON, String


class DingtalkK12StudentHistoryEntity(HistoryEntity):
    """
    k12学生历史表
    """

    __tablename__ = "st_dingtalk_k12_student_history"
    __table_args__ = {"comment": "k12学生历史表"}
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_user_id = Column(String(255), comment="远程用户id", nullable=False)
    unionid = Column(String(255), comment="unionid")
    name = Column(String(255), comment="用户名", nullable=False)
    feature = Column(JSON, comment="其他属性")


# 时间检索索引
Index(
    "idx_dingtalk_k12_student_history_time_range",
    DingtalkK12StudentHistoryEntity.id,
    DingtalkK12StudentHistoryEntity.commenced_on,
    DingtalkK12StudentHistoryEntity.ceased_on.desc(),
    unique=True,
)

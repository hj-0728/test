"""
K12部门历史表
"""

from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Text


class DingtalkK12DeptHistoryEntity(HistoryEntity):
    """
    K12部门历史表
    """

    __tablename__ = "st_dingtalk_k12_dept_history"
    __table_args__ = {"comment": "K12部门历史表"}
    dingtalk_corp_id = Column(String(40), comment="组织id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    remote_dept_id = Column(String(255), comment="远程部门id", nullable=False)
    parent_dingtalk_k12_dept_id = Column(String(40), comment="父部门id", index=True)
    contact_type = Column(String(255), comment="通讯录类型，和行业相关", nullable=False)
    dept_type = Column(String(255), comment="类型", nullable=False)
    feature = Column(Text, comment="部门的其他业务属性")
    nick = Column(String(255), comment="别名")


# 时间检索索引
Index(
    "idx_dingtalk_k12_dept_history_time_range",
    DingtalkK12DeptHistoryEntity.id,
    DingtalkK12DeptHistoryEntity.commenced_on,
    DingtalkK12DeptHistoryEntity.ceased_on.desc(),
    unique=True,
)

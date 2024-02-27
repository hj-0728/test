"""
k12部门
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from infra_dingtalk.entity.history.dingtalk_k12_dept_history import DingtalkK12DeptHistoryEntity


class DingtalkK12DeptEntity(VersionedEntity):
    """
    k12部门
    """

    __tablename__ = "st_dingtalk_k12_dept"
    __table_args__ = {"comment": "k12部门"}
    __history_entity__ = DingtalkK12DeptHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="组织id", nullable=False, index=True)
    name = Column(String(255), comment="名称", nullable=False)
    remote_dept_id = Column(String(255), comment="远程部门id", nullable=False)
    parent_dingtalk_k12_dept_id = Column(String(40), comment="父部门id", index=True)
    contact_type = Column(String(255), comment="通讯录类型，和行业相关", nullable=False)
    dept_type = Column(String(255), comment="类型", nullable=False)
    feature = Column(Text, comment="部门的其他业务属性（钉钉给的是字符串，先原样存下来）")
    nick = Column(String(255), comment="别名")

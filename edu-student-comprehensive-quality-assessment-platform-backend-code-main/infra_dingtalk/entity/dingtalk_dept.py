"""
钉钉部门
"""

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, text

from infra_dingtalk.entity.history.dingtalk_dept_history import DingtalkDeptHistoryEntity


class DingtalkDeptEntity(VersionedEntity):
    """
    钉钉部门
    """

    __tablename__ = "st_dingtalk_dept"
    __table_args__ = {"comment": "钉钉部门"}
    __history_entity__ = DingtalkDeptHistoryEntity
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_dept_id = Column(String(255), comment="远程部门id", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    parent_dingtalk_dept_id = Column(String(255), comment="父部门id", index=True)
    seq = Column(Integer, comment="序号", nullable=False, server_default=text("1"))

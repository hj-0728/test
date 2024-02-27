"""
钉钉部门历史表
"""


from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, text


class DingtalkDeptHistoryEntity(HistoryEntity):
    """
    实体类
    """

    __tablename__ = "st_dingtalk_dept_history"
    __table_args__ = {"comment": "钉钉部门历史表"}
    dingtalk_corp_id = Column(String(40), comment="钉钉组织id", nullable=False, index=True)
    remote_dept_id = Column(String(255), comment="远程部门id", nullable=False)
    name = Column(String(255), comment="名称", nullable=False)
    parent_dingtalk_dept_id = Column(String(255), comment="父部门id", index=True)
    seq = Column(Integer, comment="序号", nullable=False, server_default=text("1"))


# 时间检索索引
Index(
    "idx_dingtalk_dept_history_time_range",
    DingtalkDeptHistoryEntity.id,
    DingtalkDeptHistoryEntity.commenced_on,
    DingtalkDeptHistoryEntity.ceased_on.desc(),
    unique=True,
)

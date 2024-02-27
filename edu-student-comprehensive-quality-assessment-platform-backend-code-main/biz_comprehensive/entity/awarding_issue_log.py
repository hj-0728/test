from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from biz_comprehensive.entity.history.awarding_issue_log_history import (
    AwardingIssueLogHistoryEntity,
)


class AwardingIssueLogEntity(VersionedEntity):
    """
    发放日志
    """

    __tablename__ = "st_awarding_issue_log"
    __table_args__ = {"comment": "发放日志"}
    __history_entity__ = AwardingIssueLogHistoryEntity
    awarding_id = Column(String(40), comment="发放id", nullable=False)
    awarding_res_category = Column(
        String(255), comment="发放资源类别（DIMENSION_DEPT_TREE/ESTABLISH_ASSIGN）", nullable=False
    )
    awarding_res_id = Column(String(40), comment="发放资源id", nullable=False)
    issued_on = Column(String(40), comment="发放时间", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
    status = Column(String(255), comment="状态（ISSUED/REVOKED）", nullable=False)
    edition = Column(String(255), comment="文本，自己写第几届", nullable=False)
    grade = Column(String(255), comment="几等奖，给人自己选，并可以手工填入", nullable=False)

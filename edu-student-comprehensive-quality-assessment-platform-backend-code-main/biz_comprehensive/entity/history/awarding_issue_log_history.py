from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class AwardingIssueLogHistoryEntity(HistoryEntity):
    """
    荣誉发放记录历史
    """

    __tablename__ = "st_awarding_issue_log_history"
    __table_args__ = {"comment": "荣誉发放记录历史"}
    awarding_id = Column(String(40), comment="荣誉id", nullable=False)
    issued_res_category = Column(
        String(255), comment="发放者资源类别（DIMENSION_DEPT_TREE/ESTABLISH_ASSIGN）", nullable=False
    )
    issued_res_id = Column(String(40), comment="发放者资源id", nullable=False)
    issued_on = Column(DateTime(timezone=True), comment="发放时间", nullable=False)
    status = Column(String(255), comment="状态状态（ISSUED/REVOKED）", nullable=False)
    edition = Column(String(255), comment="文本，自己写第几届", nullable=False)
    grade = Column(String(255), comment="几等奖，给人自己选，并可以手工填入", nullable=False)


Index(
    "idx_awarding_issue_log_history_time_range",
    AwardingIssueLogHistoryEntity.id,
    AwardingIssueLogHistoryEntity.commenced_on,
    AwardingIssueLogHistoryEntity.ceased_on.desc(),
    unique=True,
)

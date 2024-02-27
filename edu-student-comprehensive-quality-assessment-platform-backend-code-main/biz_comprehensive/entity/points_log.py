from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Numeric, String, text

from biz_comprehensive.entity.history.points_log_history import PointsLogHistoryEntity


class PointsLogEntity(VersionedEntity):
    """
    积分日志
    """

    __tablename__ = "st_points_log"
    __table_args__ = {"comment": "积分日志"}
    __history_entity__ = PointsLogHistoryEntity
    owner_res_category = Column(
        String(255),
        comment="所属资源类别（班级/学生,DIMENSION_DEPT_TREE/ESTABLISHMENT_ASSIGN）",
        nullable=False,
    )
    owner_res_id = Column(String(40), comment="所属资源id", nullable=False)
    gained_points = Column(Numeric, comment="本次获得的积分", nullable=False)
    symbol_id = Column(String(40), comment="符号id", nullable=False)
    balanced_addition = Column(Numeric, comment="计算后累计正分", nullable=False)
    balanced_subtraction = Column(Numeric, comment="计算后累计负分", nullable=False)
    status = Column(String(255), comment="状态（REVOKED/CONFIRMED/REVERSED）", nullable=False)
    expired_on = Column(
        DateTime(timezone=True),
        comment="有效至，默认至无穷",
        nullable=False,
        server_default=text("'infinity'::timestamptz"),
    )
    belongs_to_period_id = Column(String(40), comment="所属期间id", nullable=False)

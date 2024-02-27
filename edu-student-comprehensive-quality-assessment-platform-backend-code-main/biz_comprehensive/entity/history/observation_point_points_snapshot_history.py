from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import ARRAY, Column, DateTime, Index, Integer, Numeric, String, Text


class ObservationPointPointsSnapshotHistoryEntity(HistoryEntity):
    """
    观测点积分快照历史
    """

    __tablename__ = "st_observation_point_points_snapshot_history"
    __table_args__ = {"comment": "观测点积分快照历史"}
    dimension_dept_tree_id = Column(
        String(40), comment="部门树id（通常是把班级的tree_id记录下来，表示这件事是发生在这个班的）", nullable=False, index=True
    )
    observation_action_id = Column(String(40), comment="观察动作id", nullable=False, index=True)
    observation_action_performer_name = Column(String(40), comment="观察动作执行者的名字", nullable=False)
    observation_on = Column(DateTime(timezone=True), comment="观察时间", nullable=False, index=True)
    observation_point_log_id = Column(String(40), comment="观察点日志id", nullable=False, index=True)
    observee_name = Column(String(255), comment="被观察者名字", nullable=False)
    observation_point_name = Column(String(255), comment="观测点名字", nullable=False)
    observation_point_category = Column(String(255), comment="观测点类型", nullable=False)
    observation_point_icon = Column(Text, comment="观测点icon", nullable=False)
    scene_ids = Column(ARRAY(String(40)), comment="场景信息列表", nullable=True)
    points_log_id = Column(String(40), comment="积分日志id", nullable=False, index=True)
    owner_res_category = Column(String(40), comment="获得者类型", nullable=False)
    owner_res_id = Column(String(40), comment="获得者id", nullable=False)
    owner_name = Column(String(255), comment="获得者名称", nullable=False)
    owner_avatar = Column(Text, comment="获得者头像", nullable=False)
    gained_points = Column(Numeric, comment="获得积分", nullable=False)
    symbol_code = Column(String(255), comment="获得者头像", nullable=False)
    numeric_precision = Column(Integer, comment="精度", nullable=False)
    belongs_to_period_id = Column(String(255), comment="所属周期id（通常是学期）", nullable=False, index=True)


Index(
    "idx_observation_point_points_snapshot_history_owner",
    ObservationPointPointsSnapshotHistoryEntity.owner_res_category,
    ObservationPointPointsSnapshotHistoryEntity.owner_res_id,
)

Index(
    "idx_observation_point_points_snapshot_history_time_range",
    ObservationPointPointsSnapshotHistoryEntity.id,
    ObservationPointPointsSnapshotHistoryEntity.commenced_on,
    ObservationPointPointsSnapshotHistoryEntity.ceased_on.desc(),
    unique=True,
)

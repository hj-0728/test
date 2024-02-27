from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String, Text


class TodoBatchHistoryEntity(HistoryEntity):
    """
    待办批次历史
    """

    __tablename__ = "st_todo_batch_history"
    __table_args__ = {"comment": "待办批次历史"}
    title = Column(String(255), comment="标题", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
    owner_res_category = Column(String(255), comment="所有者资源类型", nullable=False)
    owner_res_id = Column(String(40), comment="所有者资源id", nullable=False)


Index(
    "idx_todo_batch_history_time_range",
    TodoBatchHistoryEntity.id,
    TodoBatchHistoryEntity.commenced_on,
    TodoBatchHistoryEntity.ceased_on.desc(),
    unique=True,
)

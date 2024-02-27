from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, Text

from biz_comprehensive.entity.history.todo_batch_history import TodoBatchHistoryEntity


class TodoBatchEntity(VersionedEntity):
    """
    待办批次
    """

    __tablename__ = "st_todo_batch"
    __table_args__ = {"comment": "待办批次"}
    __history_entity__ = TodoBatchHistoryEntity
    title = Column(String(255), comment="标题", nullable=False)
    comment = Column(Text, comment="备注", nullable=True)
    owner_res_category = Column(String(255), comment="所有者资源类型", nullable=False)
    owner_res_id = Column(String(40), comment="所有者资源id", nullable=False)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import ARRAY, Column, Integer, String

from biz_comprehensive.entity.history.todo_history import TodoHistoryEntity


class TodoEntity(VersionedEntity):
    """
    待办
    """

    __tablename__ = "st_todo"
    __table_args__ = {"comment": "待办"}
    __history_entity__ = TodoHistoryEntity
    todo_batch_id = Column(String(40), comment="代办事项批次id", nullable=False)
    title = Column(String(255), comment="标题", nullable=False)
    result_value_type = Column(String(255), comment="结果值类型（NUM/STRING）", nullable=False)
    numeric_precision = Column(Integer, comment="数值精度", nullable=True)
    string_options = Column(ARRAY(String(255)), comment="字符可选项", nullable=True)

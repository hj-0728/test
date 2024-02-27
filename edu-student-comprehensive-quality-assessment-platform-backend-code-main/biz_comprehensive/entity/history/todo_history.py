from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import ARRAY, Column, Index, Integer, String


class TodoHistoryEntity(HistoryEntity):
    """
    代办事项历史
    """

    __tablename__ = "st_todo_history"
    __table_args__ = {"comment": "代办事项历史"}
    todo_batch_id = Column(String(40), comment="代办事项批次id", nullable=False)
    title = Column(String(255), comment="标题", nullable=False)
    result_value_type = Column(String(255), comment="结果值类型（NUM/STRING）", nullable=False)
    numeric_precision = Column(Integer, comment="数值精度", nullable=True)
    string_options = Column(ARRAY(String(255)), comment="字符可选项", nullable=True)


Index(
    "idx_todo_history_time_range",
    TodoHistoryEntity.id,
    TodoHistoryEntity.commenced_on,
    TodoHistoryEntity.ceased_on.desc(),
    unique=True,
)

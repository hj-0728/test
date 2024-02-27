from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, DateTime, Index, String


class TodoTaskHistoryEntity(HistoryEntity):
    """
    待办事项
    """

    __tablename__ = "st_todo_task_history"
    __table_args__ = {"comment": "待办事项"}
    title = Column(String(255), comment="标题", nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=True, comment="什么时候做完的")
    assign_category = Column(String(255), comment="分配资源类型", nullable=False)
    assign_id = Column(String(255), comment="分配资源id", nullable=False)
    trigger_category = Column(String(255), comment="触发资源类型", nullable=False)
    trigger_id = Column(String(255), comment="触发资源id", nullable=False)
    completed_by = Column(String(255), comment="谁完成了这个任务", nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="什么时候做完的")
    comments = Column(String(255), comment="描述", nullable=True)


Index(
    "idx_todo_task_history_assign",
    TodoTaskHistoryEntity.id,
    TodoTaskHistoryEntity.assign_category,
    TodoTaskHistoryEntity.assign_id,
)

Index(
    "idx_todo_task_history_trigger",
    TodoTaskHistoryEntity.id,
    TodoTaskHistoryEntity.trigger_category,
    TodoTaskHistoryEntity.trigger_id,
)

Index(
    "idx_todo_task_history_time_range",
    TodoTaskHistoryEntity.id,
    TodoTaskHistoryEntity.begin_at,
    TodoTaskHistoryEntity.end_at.desc(),
    unique=True,
)

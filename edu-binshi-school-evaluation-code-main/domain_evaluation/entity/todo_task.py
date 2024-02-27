from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, DateTime, Index, String

from domain_evaluation.entity.history.todo_task_history import TodoTaskHistoryEntity


class TodoTaskEntity(VersionedEntity):
    """
    待办事项
    """

    __tablename__ = "st_todo_task"
    __table_args__ = {"comment": "待办事项"}
    __history_entity__ = TodoTaskHistoryEntity
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
    "idx_todo_task_assign",
    TodoTaskEntity.id,
    TodoTaskEntity.assign_category,
    TodoTaskEntity.assign_id,
)

Index(
    "idx_todo_task_trigger",
    TodoTaskEntity.id,
    TodoTaskEntity.trigger_category,
    TodoTaskEntity.trigger_id,
)

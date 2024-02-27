from typing import Optional

from domain_evaluation.model.todo_task_model import TodoTaskModel


class TodoTaskPageViewModel(TodoTaskModel):
    """
    待办事项
    """

    plan_name: Optional[str]
    completed_people_name: Optional[str]

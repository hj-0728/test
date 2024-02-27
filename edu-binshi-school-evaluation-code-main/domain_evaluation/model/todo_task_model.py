from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import Field
from infra_utility.datetime_helper import local_now

from infra_basic.basic_model import VersionedModel


class EnumTodoTaskAssignCategory(Enum):
    """
    待办事项分配资源类型
    """

    ROLE = "角色"


class EnumTodoTaskTriggerCategory(Enum):
    """
    待办事项触发资源类型
    """

    EVALUATION_CRITERIA_PLAN = "评价计划"


class TodoTaskModel(VersionedModel):
    """
    待办事项
    """

    title: Optional[str]
    generated_at: datetime = Field(default_factory=local_now)
    assign_category: Optional[str]
    assign_id: Optional[str]
    trigger_category: Optional[str]
    trigger_id: Optional[str]
    completed_by: Optional[str]
    completed_at: Optional[datetime]

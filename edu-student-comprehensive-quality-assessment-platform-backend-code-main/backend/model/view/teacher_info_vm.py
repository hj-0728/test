from typing import Optional

from infra_basic.basic_model import BasePlusModel


class TeacherInfoViewModel(BasePlusModel):
    id: str
    name: str
    avatar: Optional[str]
    is_taught: bool  # 是否任教
    current_period_name: Optional[str]  # 当前学期名称

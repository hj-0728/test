"""
老师任教班级
"""
from typing import Optional

from infra_basic.basic_model import BasicModel


class TeacherClassViewModel(BasicModel):
    name: str
    avatar: str
    student_count: int
    points_count: int
    dimension_dept_tree_id: str

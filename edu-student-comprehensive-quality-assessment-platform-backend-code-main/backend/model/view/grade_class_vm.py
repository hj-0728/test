from typing import List, Optional

from infra_basic.basic_model import BasicModel


class ClassViewModel(BasicModel):
    name: str
    avatar: str
    dimension_dept_tree_id: str


class GradeClassListViewModel(BasicModel):
    name: str
    class_list: List[ClassViewModel]


class GradeClassViewModel(BasicModel):
    name: str
    parent_dept_id: str
    parent_name: str
    avatar: str
    dimension_dept_tree_id: str

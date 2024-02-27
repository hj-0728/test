from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class ClassStudentViewModel(BasePlusModel):
    id: str
    establishment_assign_id: str
    name: str
    avatar: str
    balanced_addition: int
    balanced_subtraction: int
    rating_symbol: Optional[str]  # 等级符号， 如星星，月亮，太阳等
    rating_symbol_count: Optional[int]  # 等级符号数量， 如2颗星


class ClassIndexStudentViewModel(BasePlusModel):
    index: str
    student_list: List[ClassStudentViewModel]


class ClassStudentListViewModel(BasePlusModel):
    id: str
    avatar: str
    student_count: int
    balanced_addition: int
    balanced_subtraction: int

    student_index_list: List[ClassIndexStudentViewModel] = []
    student_list: List[ClassStudentViewModel] = []

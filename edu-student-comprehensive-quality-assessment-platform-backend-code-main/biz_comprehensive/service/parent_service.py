from typing import List

from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from biz_comprehensive.repository.parent_repository import ParentRepository


class ParentService:
    def __init__(self, parent_repository: ParentRepository):
        self.__parent_repository = parent_repository

    def get_child_list(self, parent_people_id: str) -> List[StudentInfoViewModel]:
        """
        获取孩子列表
        """
        return self.__parent_repository.fetch_child_list(parent_people_id)

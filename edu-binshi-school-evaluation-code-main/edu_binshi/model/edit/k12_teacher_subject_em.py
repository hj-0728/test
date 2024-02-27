from datetime import datetime
from typing import List

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.datetime_helper import local_now
from pydantic import Field

from edu_binshi.model.k12_teacher_subject_model import K12TeacherSubjectModel
from edu_binshi.model.view.k12_teacher_subject_vm import K12TeacherSubjectVm


class K12TeacherSubjectEm(BasePlusModel):
    """
    k12 教师科目Em
    """

    people_id: str
    dimension_dept_tree_id: str
    subject_name_list: List[str]

    existed_teacher_subject: List[K12TeacherSubjectVm] = []

    current_time: datetime = Field(default_factory=local_now)

    loop: int = 0

    def exists_people_ids(self) -> List[str]:
        return [item.people_id for item in self.existed_teacher_subject]

    def to_k12_teacher_subject(self, subject_id: str) -> K12TeacherSubjectModel:
        return K12TeacherSubjectModel(
            people_id=self.people_id,
            dimension_dept_tree_id=self.dimension_dept_tree_id,
            subject_id=subject_id,
            start_at=self.current_time,
        )

    def update_loop(self):
        if self.existed_teacher_subject:
            self.loop = 1

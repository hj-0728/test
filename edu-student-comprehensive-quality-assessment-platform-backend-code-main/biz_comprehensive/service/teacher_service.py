from collections import defaultdict
from datetime import datetime
from typing import List

from dateutil.relativedelta import MO, relativedelta
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.datetime_helper import local_now

from backend.model.view.grade_class_vm import GradeClassListViewModel
from backend.model.view.teacher_class_vm import TeacherClassViewModel
from backend.model.view.teacher_info_vm import TeacherInfoViewModel
from biz_comprehensive.model.param.teacher_observation_query_params import (
    TeacherObservationQueryParams,
)
from biz_comprehensive.model.period_model import PeriodModel
from biz_comprehensive.model.search_history_model import EnumSearchScene, SearchHistoryModel
from biz_comprehensive.model.view.observation_class_vm import ObservationClassViewModel
from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from biz_comprehensive.repository.teacher_repository import TeacherRepository
from biz_comprehensive.service.search_history_service import SearchHistoryService


class TeacherService:
    def __init__(
        self,
        teacher_repository: TeacherRepository,
        search_history_service: SearchHistoryService,
    ):
        self.__teacher_repository = teacher_repository
        self.__search_history_service = search_history_service

    def get_teacher_class_list(
        self, teacher_id: str, period_id: str
    ) -> List[TeacherClassViewModel]:
        """
        获取老师的班级列表
        """
        # 获取本周周一的时间
        monday = self.get_this_week_monday()
        teacher_class_list = self.__teacher_repository.fetch_teacher_class_list(
            people_id=teacher_id, points_due_on=monday, period_id=period_id
        )
        return teacher_class_list

    @staticmethod
    def get_this_week_monday() -> datetime:
        """
        获取本周周一的时间
        """
        today = datetime.today()
        this_week_monday = today + relativedelta(weekday=MO(-1))
        this_week_monday = this_week_monday.replace(hour=0, minute=0, second=0, microsecond=0)
        return this_week_monday

    def get_school_grade_class_list(self) -> List[GradeClassListViewModel]:
        """
        获取学校的班级列表
        """
        school_class_list = self.__teacher_repository.fetch_grade_class_list()
        grade_to_class_map = defaultdict(list)
        for school_class in school_class_list:
            key = (school_class.parent_dept_id, school_class.parent_name)
            grade_to_class_map[key].append(school_class)
        res = []
        for grade, class_list in grade_to_class_map.items():
            grade_class = GradeClassListViewModel(
                **{"id": grade[0], "name": grade[1][:3], "class_list": class_list}
            )
            res.append(grade_class)
        return res

    def search_student(
        self, people_id: str, search_text: str, transaction: Transaction
    ) -> List[StudentInfoViewModel]:
        """
        搜索学生
        """
        self.__search_history_service.add_search_history(
            data=SearchHistoryModel(
                owner_people_id=people_id,
                search_content=search_text,
                search_on=local_now(),
                search_scene=EnumSearchScene.MOBILE_STUDENT.name,
            ),
            transaction=transaction,
        )
        return self.__teacher_repository.fetch_student_by_name_keyword(search_text)

    def get_teacher_info(self, people_id: str, period: PeriodModel) -> TeacherInfoViewModel:
        """
        获取老师信息
        :param people_id:
        :param period:
        :return:
        """
        teacher = self.__teacher_repository.fetch_teacher_info(people_id)
        teacher.current_period_name = period.name
        return teacher

    def get_observation_class_list(
        self, params: TeacherObservationQueryParams
    ) -> List[ObservationClassViewModel]:
        """
        获取观察班级列表
        """
        return self.__teacher_repository.fetch_observation_class_list(params)

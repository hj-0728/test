from collections import defaultdict

from pypinyin import lazy_pinyin

from biz_comprehensive.model.edit.load_class_student_em import (
    EnumSortMethods,
    LoadClassStudentEditModel,
)
from biz_comprehensive.model.view.class_student_vm import (
    ClassIndexStudentViewModel,
    ClassStudentListViewModel,
)
from biz_comprehensive.repository.student_points_log_repository import StudentPointsLogRepository
from biz_comprehensive.repository.symbol_repository import SymbolRepository
from biz_comprehensive.service.symbol_service import SymbolService
from infra_backbone.service.dept_service import DeptService


class StudentPointsLogService:
    def __init__(
        self,
        symbol_repository: SymbolRepository,
        student_points_log_repository: StudentPointsLogRepository,
        symbol_service: SymbolService,
        dept_service: DeptService,
    ):
        self.__symbol_repository = symbol_repository
        self.__student_points_log_repository = student_points_log_repository
        self.__symbol_service = symbol_service
        self.__dept_service = dept_service

    def load_class_student_points(
        self, data: LoadClassStudentEditModel
    ) -> ClassStudentListViewModel:
        """
        加载班级学生积分
        :param data:
        :return:
        """
        student_list = self.__student_points_log_repository.fetch_class_student_with_points(
            tree_id=data.tree_id, period_id=data.period_id
        )
        symbol_list = self.__symbol_repository.fetch_rating_show_symbol_exchange()
        class_balanced_addition, class_balanced_subtraction = 0, 0
        student_dict = defaultdict(list)
        for student in student_list:
            rating_symbol, rating_symbol_count = self.__symbol_service.points_exchange_rating_show(
                points=student.balanced_addition, symbol_list=symbol_list
            )
            student.rating_symbol = rating_symbol
            student.rating_symbol_count = rating_symbol_count
            class_balanced_addition += student.balanced_addition
            class_balanced_subtraction += student.balanced_subtraction

            if data.sort_methods == EnumSortMethods.INITIALS_NAME.name:
                # 在这个地方把学生按照initials_name从A到Z聚合排序
                initials_name = lazy_pinyin(student.name)[0][0].upper()
                student_dict[initials_name].append(student)

        student_index_list = []
        if data.sort_methods == EnumSortMethods.INITIALS_NAME.name:
            student_index_list = sorted(
                [
                    ClassIndexStudentViewModel(index=k, student_list=v)
                    for k, v in student_dict.items()
                ],
                key=lambda x: x.index,
            )
        class_avatar = self.__dept_service.get_dept_avatar_url(tree_id=data.tree_id)
        result = ClassStudentListViewModel(
            id=data.tree_id,
            avatar=class_avatar,
            student_count=len(student_list),
            balanced_addition=class_balanced_addition,
            balanced_subtraction=class_balanced_subtraction,
            student_index_list=student_index_list,
        )
        if data.sort_methods != EnumSortMethods.INITIALS_NAME.name:
            result.student_list = student_list
        return result

from datetime import datetime
from typing import List, Optional, Tuple, Union

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from edu_binshi.data.query_params.teacher_query_params import TeacherPageQueryParams
from edu_binshi.model.edit.k12_teacher_subject_em import K12TeacherSubjectEm
from edu_binshi.model.k12_teacher_subject_model import K12TeacherSubjectModel
from edu_binshi.model.subject_model import SubjectModel
from edu_binshi.model.view.k12_teacher_subject_vm import (
    K12TeacherSubjectFiltersVm,
    K12TeacherSubjectVm,
)
from edu_binshi.repository.k12_teacher_subject_repository import K12TeacherSubjectRepository
from edu_binshi.repository.subject_repository import SubjectRepository
from infra_backbone.model.capacity_model import EnumCapacityCode


class K12TeacherSubjectService:
    def __init__(
        self,
        k12_teacher_subject_repository: K12TeacherSubjectRepository,
        subject_repository: SubjectRepository,
    ):
        self.__k12_teacher_subject_repository = k12_teacher_subject_repository
        self.__subject_repository = subject_repository

    def get_k12_teacher_list_page(
        self,
        params: TeacherPageQueryParams,
    ):
        """
        获取学生分页
        :return:
        """
        return self.__k12_teacher_subject_repository.get_k12_teacher_list_page(params=params)

    def get_k12_teacher_subject_detail(
        self,
        people_id: str,
        dimension_dept_tree_id: str,
    ) -> List[K12TeacherSubjectVm]:
        """
        获取教师科目列表
        """
        return self.__k12_teacher_subject_repository.get_k12_teacher_subject_vm_list(
            people_id=people_id,
            dimension_dept_tree_id=dimension_dept_tree_id,
        )

    def get_subject_list(self):
        """
        获取科目列表
        """
        return self.__subject_repository.get_subject_list()

    def get_capacity_and_subject_filters(self):
        """
        获取能力和科目筛选列表
        """
        subject_list = self.__subject_repository.get_subject_list()
        subject_filters = [
            {"text": subject.name, "value": subject.name} for subject in subject_list
        ]
        subject_filters.append({"text": '暂无', "value": 'NONE'})
        capacity_filters = [
            {
                "text": EnumCapacityCode.TEACHER.value,
                "value": EnumCapacityCode.TEACHER.value,
            },
            {
                "text": EnumCapacityCode.HEAD_TEACHER.value,
                "value": EnumCapacityCode.HEAD_TEACHER.value,
            },
        ]
        return K12TeacherSubjectFiltersVm(
            subject_filters=subject_filters,
            capacity_filters=capacity_filters,
        )

    def save_k12_teacher_subject(
        self,
        k12_teacher_subject_em: K12TeacherSubjectEm,
        transaction: Transaction,
    ) -> Tuple[bool, Union[List[str], Optional[K12TeacherSubjectEm]]]:
        """
        设置教师科目
        """
        self.delete_old_teacher_subject(
            old_teacher_subject_list=k12_teacher_subject_em.existed_teacher_subject,
            finish_at=k12_teacher_subject_em.current_time,
            transaction=transaction,
        )

        origin_list = self.__k12_teacher_subject_repository.get_k12_teacher_subject_vm_list(
            people_id=k12_teacher_subject_em.people_id,
            dimension_dept_tree_id=k12_teacher_subject_em.dimension_dept_tree_id,
        )
        origin_subject_id_list = [x.subject_id for x in origin_list]
        new_subject_id_list = []
        existed_teacher_subject = []
        for subject_name in k12_teacher_subject_em.subject_name_list:
            subject_id, new = self.update_subject(
                subject_name=subject_name, transaction=transaction
            )
            if not new:
                self.check_teacher_subject_can_add(
                    k12_teacher_subject_em=k12_teacher_subject_em,
                    subject_id=subject_id,
                    subject_name=subject_name,
                    existed_teacher_subject=existed_teacher_subject,
                )
            if existed_teacher_subject:
                continue

            if subject_id not in origin_subject_id_list:
                self.__k12_teacher_subject_repository.insert_k12_teacher_subject(
                    k12_teacher_subject=k12_teacher_subject_em.to_k12_teacher_subject(
                        subject_id=subject_id
                    ),
                    transaction=transaction,
                )
            new_subject_id_list.append(subject_id)
        if existed_teacher_subject:
            k12_teacher_subject_em.existed_teacher_subject = existed_teacher_subject
            return False, k12_teacher_subject_em

        for origin_subject in origin_list:
            if origin_subject.subject_id not in new_subject_id_list:
                old_k12_teacher_subject = origin_subject.cast_to(cast_type=K12TeacherSubjectModel)
                old_k12_teacher_subject.finish_at = k12_teacher_subject_em.current_time
                self.__k12_teacher_subject_repository.update_k12_teacher_subject(
                    k12_teacher_subject=old_k12_teacher_subject,
                    transaction=transaction,
                    limited_col_list=["finish_at"],
                )
        return True, new_subject_id_list

    def update_subject(self, subject_name: str, transaction: Transaction) -> Tuple[str, bool]:
        """
        更新科目
        """
        subject = self.__subject_repository.get_subject_by_name(name=subject_name)
        if not subject:
            subject_id = self.__subject_repository.insert_subject(
                subject=SubjectModel(name=subject_name, is_activated=True),
                transaction=transaction,
            )
            return subject_id, True
        if subject.is_activated is False:
            subject.is_activated = True
            self.__subject_repository.update_subject(subject=subject, transaction=transaction)
        return subject.id, False

    def check_teacher_subject_can_add(
        self,
        k12_teacher_subject_em: K12TeacherSubjectEm,
        subject_id: str,
        subject_name: str,
        existed_teacher_subject: List[K12TeacherSubjectVm],
    ):
        """
        检查教师科目是否可以添加
        """
        teacher = self.__k12_teacher_subject_repository.fetch_class_subject_other_teacher(
            subject_id=subject_id,
            people_id=k12_teacher_subject_em.people_id,
            dimension_dept_tree_id=k12_teacher_subject_em.dimension_dept_tree_id,
        )
        if (
            teacher
            and k12_teacher_subject_em.existed_teacher_subject
            and teacher.people_id not in k12_teacher_subject_em.exists_people_ids()
        ):
            # 因为不能一直检查到有其他老师在任教了，就返回到前端去给用户确认，这样不是死循环了
            # 所以k12_teacher_subject_em中有已存在的老师了，说明当前已经是第二轮了
            raise BusinessError("数据已发生改变，请重新提交！")
        if teacher and k12_teacher_subject_em.loop == 0:
            # 只有第一次提交的时候才需要把已任教的老师信息返回
            # 不能判断existed_teacher_subject是否为空，因为可能是循环中的第二个数据
            teacher.subject_name = subject_name
            existed_teacher_subject.append(teacher)

    def delete_old_teacher_subject(
        self,
        old_teacher_subject_list: List[K12TeacherSubjectVm],
        finish_at: datetime,
        transaction: Transaction,
    ):
        """
        删除教师科目
        """
        for old_teacher_subject in old_teacher_subject_list:
            db_data = self.__k12_teacher_subject_repository.fetch_k12_teacher_subject_by_id(
                k12_teacher_subject_id=old_teacher_subject.id
            )
            if not db_data or db_data.version != old_teacher_subject.version:
                raise BusinessError("数据已发生改变，请刷新页面重新提交！")
            teacher_subject = old_teacher_subject.cast_to(cast_type=K12TeacherSubjectModel)
            teacher_subject.finish_at = finish_at
            self.__k12_teacher_subject_repository.update_k12_teacher_subject(
                k12_teacher_subject=teacher_subject,
                transaction=transaction,
                limited_col_list=["finish_at"],
            )

    def sync_k12_teacher_subject(self, transaction: Transaction):
        """
        同步老师教授课程，因为有些老师从班级离开，需要删除数据
        :param transaction:
        :return:
        """

        need_delete_data = self.__k12_teacher_subject_repository.get_need_delete_k12_teacher_subject()

        for k12_teacher_subject in need_delete_data:
            k12_teacher_subject.finish_at = local_now()
            self.__k12_teacher_subject_repository.update_k12_teacher_subject(
                k12_teacher_subject=k12_teacher_subject,
                transaction=transaction
            )


import logging
from typing import Dict

from infra_basic.transaction import Transaction

from infra_dingtalk.data.agent_plugin.dingtalk_student import DingtalkStudent
from infra_dingtalk.model.dingtalk_k12_dept_student_model import DingtalkK12DeptStudentModel
from infra_dingtalk.model.dingtalk_k12_family_relationship_model import (
    DingtalkK12FamilyRelationshipModel,
)
from infra_dingtalk.model.dingtalk_k12_parent_model import DingtalkK12ParentModel
from infra_dingtalk.model.dingtalk_k12_student_model import DingtalkK12StudentModel
from infra_dingtalk.model.view.dingtalk_k12_dept_with_admins_vm import (
    DingtalkK12DeptWithAdminsViewModel,
)
from infra_dingtalk.model.view.dingtalk_k12_student_detail_vm import (
    DingtalkK12StudentDetailViewModel,
)
from infra_dingtalk.repository.dingtalk_k12_dept_student_repository import (
    DingtalkK12DeptStudentRepository,
)
from infra_dingtalk.repository.dingtalk_k12_family_relationship_repository import (
    DingtalkK12FamilyRelationshipRepository,
)
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_k12_student_repository import DingtalkK12StudentRepository


class K12SyncStudentService:
    """
    同步k12部门
    """

    def __init__(
        self,
        dingtalk_k12_student_repository: DingtalkK12StudentRepository,
        dingtalk_k12_parent_repository: DingtalkK12ParentRepository,
        dingtalk_k12_family_relationship_repository: DingtalkK12FamilyRelationshipRepository,
        dingtalk_k12_dept_student_repository: DingtalkK12DeptStudentRepository,
    ):
        self._dingtalk_k12_student_repository = dingtalk_k12_student_repository
        self._dingtalk_k12_parent_repository = dingtalk_k12_parent_repository
        self._dingtalk_k12_family_relationship_repository = (
            dingtalk_k12_family_relationship_repository
        )
        self._dingtalk_k12_dept_student_repository = dingtalk_k12_dept_student_repository

        # 为了最小的改动
        self._dingtalk_corp_id = None
        self._remote_student_dict = None
        self._db_k12_dept_dict = None
        self._transaction = None
        self._db_student_dict = None
        self._db_parent_dict = None

    def super_init_attr(
        self,
        dingtalk_corp_id: str,
        remote_student_dict: Dict[str, DingtalkStudent],
        db_k12_dept_dict: Dict[int, DingtalkK12DeptWithAdminsViewModel],
        transaction: Transaction,
    ):
        self._dingtalk_corp_id = dingtalk_corp_id
        self._remote_student_dict = remote_student_dict
        self._transaction = transaction
        self._db_k12_dept_dict = db_k12_dept_dict
        self._db_student_dict = self.__get_db_student_dict()
        self._db_parent_dict = self.__get_db_parent_dict()

    def __get_db_student_dict(
        self,
    ) -> Dict[str, DingtalkK12StudentDetailViewModel]:
        """
        获取数据库中学生以远程id为键的字典
        """
        db_student_list = (
            self._dingtalk_k12_student_repository.fetch_dingtalk_k12_student_with_parents(
                dingtalk_corp_id=self._dingtalk_corp_id
            )
        )
        return {x.remote_user_id: x for x in db_student_list}

    def __get_db_parent_dict(self) -> Dict[str, DingtalkK12ParentModel]:
        """
        获取数据库中家长以远程id为键的字典
        """

        data: Dict[str, DingtalkK12ParentModel] = {}
        for student in self._db_student_dict.values():
            for parent in student.parent_list:
                data[parent.remote_user_id] = parent
        return data

    def sync_remote_parent_to_db(
        self,
        dingtalk_corp_id: str,
        remote_student_dict: Dict[str, DingtalkStudent],
        db_k12_dept_dict: Dict[int, DingtalkK12DeptWithAdminsViewModel],
        transaction: Transaction,
    ):
        """
        同步远程的家长到数据库
        """
        self.super_init_attr(
            dingtalk_corp_id=dingtalk_corp_id,
            remote_student_dict=remote_student_dict,
            db_k12_dept_dict=db_k12_dept_dict,
            transaction=transaction,
        )
        existed_parent_user_ids = []
        for student in self._remote_student_dict.values():
            for parent in student.parents:
                if parent.from_userid in existed_parent_user_ids:
                    continue
                existed_parent_user_ids.append(parent.from_userid)
                db_parent = self._db_parent_dict.get(parent.from_userid)
                if not db_parent:
                    new_parent = parent.to_dingtalk_k12_parent_em(
                        dingtalk_corp_id=self._dingtalk_corp_id
                    )
                    new_parent.id = self._dingtalk_k12_parent_repository.insert_dingtalk_k12_parent(
                        parent=new_parent, transaction=self._transaction
                    )
                    self._db_parent_dict[parent.from_userid] = new_parent.cast_to(
                        cast_type=DingtalkK12ParentModel
                    )
                elif parent.unique_dict() != db_parent.unique_dict():
                    new_parent = parent.to_dingtalk_k12_parent_em(
                        dingtalk_corp_id=self._dingtalk_corp_id
                    )
                    new_parent.id = db_parent.id
                    new_parent.version = db_parent.version
                    self._dingtalk_k12_parent_repository.update_dingtalk_k12_parent(
                        parent=new_parent, transaction=self._transaction
                    )
        for db_parent in self._db_parent_dict.values():
            if db_parent.remote_user_id not in existed_parent_user_ids:
                self._dingtalk_k12_parent_repository.delete_dingtalk_k12_parent(
                    parent_id=db_parent.id, transaction=self._transaction
                )

    def sync_remote_student_to_db(self):
        """
        同步远程的学生到数据库
        """
        for remote_stu_id, remote_student in self._remote_student_dict.items():
            db_student = self._db_student_dict.get(remote_stu_id)
            if not db_student:
                self.__add_dingtalk_k12_student(remote_student=remote_student)
            else:
                self.__update_dingtalk_k12_student(
                    remote_student=remote_student, db_student=db_student
                )
                self.__update_dingtalk_k12_dept_student(
                    remote_student=remote_student, db_student=db_student
                )
                self.__update_dingtalk_k12_student_family(
                    remote_student=remote_student, db_student=db_student
                )
        for db_student in self._db_student_dict.values():
            if not self._remote_student_dict.get(db_student.remote_user_id):
                self._dingtalk_k12_student_repository.delete_dingtalk_k12_student(
                    dingtalk_k12_student_id=db_student.id,
                    transaction=self._transaction,
                )

    def __add_dingtalk_k12_student(self, remote_student: DingtalkStudent):
        """
        添加k12学生
        """
        new_stu = remote_student.to_dingtalk_k12_student_em(dingtalk_corp_id=self._dingtalk_corp_id)
        new_stu.id = self._dingtalk_k12_student_repository.insert_dingtalk_k12_student(
            student=new_stu, transaction=self._transaction
        )
        for dept_id in remote_student.department:
            db_dept = self._db_k12_dept_dict.get(dept_id)
            if not db_dept:
                logging.error(f"添加学生时未找到id为【{dept_id}】的部门")
                continue
            self._dingtalk_k12_dept_student_repository.insert_dingtalk_k12_dept_student(
                dept_student=DingtalkK12DeptStudentModel(
                    dingtalk_k12_student_id=new_stu.id,
                    dingtalk_k12_dept_id=db_dept.id,
                ),
                transaction=self._transaction,
            )
        for parent in remote_student.parents:
            db_parent = self._db_parent_dict.get(parent.from_userid)
            if not db_parent:
                logging.error(f"未找到id为【{parent.from_userid}】的家长")
                continue
            self._dingtalk_k12_family_relationship_repository.insert_dingtalk_k12_family_relationship(
                family=parent.to_family_relationship_em(
                    student_id=new_stu.id, parent_id=db_parent.id
                ),
                transaction=self._transaction,
            )

    def __update_dingtalk_k12_student(
        self,
        remote_student: DingtalkStudent,
        db_student: DingtalkK12StudentDetailViewModel,
    ):
        """
        更新学生
        """

        if remote_student.name != db_student.name:
            db_student.name = remote_student.name
            self._dingtalk_k12_student_repository.update_dingtalk_k12_student(
                student=db_student.cast_to(cast_type=DingtalkK12StudentModel),
                transaction=self._transaction,
            )

    def __update_dingtalk_k12_dept_student(
        self,
        remote_student: DingtalkStudent,
        db_student: DingtalkK12StudentDetailViewModel,
    ):
        """
        更新k12部门学生关系
        """
        for dept_id in remote_student.department:
            if dept_id not in db_student.remote_dept_ids:
                db_dept = self._db_k12_dept_dict.get(dept_id)
                if not db_dept:
                    logging.error(f"添加学生时未找到id为【{dept_id}】的部门")
                    continue
                self._dingtalk_k12_dept_student_repository.insert_dingtalk_k12_dept_student(
                    dept_student=DingtalkK12DeptStudentModel(
                        dingtalk_k12_student_id=db_student.id,
                        dingtalk_k12_dept_id=db_dept.id,
                    ),
                    transaction=self._transaction,
                )
        for db_stu_dept in db_student.dept_list:
            if db_stu_dept.remote_dept_id not in remote_student.department:
                self._dingtalk_k12_dept_student_repository.delete_dingtalk_k12_dept_student(
                    dept_student_id=db_stu_dept.id,
                    transaction=self._transaction,
                )

    def __update_dingtalk_k12_student_family(
        self,
        remote_student: DingtalkStudent,
        db_student: DingtalkK12StudentDetailViewModel,
    ):
        """
        更新k12学生家长关系
        """
        existed_parent_user_ids = []
        for remote_parent in remote_student.parents:
            existed = False
            existed_parent_user_ids.append(remote_parent.from_userid)
            for db_rel in db_student.relationship_list:
                if remote_parent.from_userid == db_rel.parent_remote_user_id:
                    existed = True
                    if remote_parent.relation_name == db_rel.relationship_name:
                        continue
                    db_rel.relationship_name = remote_parent.relation_name
                    self._dingtalk_k12_family_relationship_repository.update_dingtalk_k12_family_relationship(
                        family=db_rel.cast_to(cast_type=DingtalkK12FamilyRelationshipModel),
                        transaction=self._transaction,
                    )
            if not existed:
                db_parent = self._db_parent_dict.get(remote_parent.from_userid)
                if not db_parent:
                    logging.error(f"未找到id为【{remote_parent.from_userid}】的家长")
                    continue
                self._dingtalk_k12_family_relationship_repository.insert_dingtalk_k12_family_relationship(
                    family=remote_parent.to_family_relationship_em(
                        student_id=db_student.id, parent_id=db_parent.id
                    ),
                    transaction=self._transaction,
                )
        for db_rel in db_student.relationship_list:
            if db_rel.parent_remote_user_id not in existed_parent_user_ids:
                self._dingtalk_k12_family_relationship_repository.delete_dingtalk_k12_family_relationship(
                    family_id=db_rel.id, transaction=self._transaction
                )

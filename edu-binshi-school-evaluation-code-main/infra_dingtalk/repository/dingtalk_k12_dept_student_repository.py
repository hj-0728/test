from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_k12_dept_student import DingtalkK12DeptStudentEntity
from infra_dingtalk.model.dingtalk_k12_dept_student_model import DingtalkK12DeptStudentModel


class DingtalkK12DeptStudentRepository(BasicRepository):
    """
    钉钉 k12 部门、学生
    """

    def insert_dingtalk_k12_dept_student(
        self, dept_student: DingtalkK12DeptStudentModel, transaction: Transaction
    ):
        """
        插入k12的部门学生
        """
        self._insert_versioned_entity_by_model(
            entity_cls=DingtalkK12DeptStudentEntity,
            entity_model=dept_student,
            transaction=transaction,
        )

    def delete_dingtalk_k12_dept_student(self, dept_student_id: str, transaction: Transaction):
        """
        删除k12部门学生关系
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkK12DeptStudentEntity,
            entity_id=dept_student_id,
            transaction=transaction,
        )

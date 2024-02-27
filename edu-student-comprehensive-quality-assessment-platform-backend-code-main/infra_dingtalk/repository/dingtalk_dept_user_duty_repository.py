from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_dept_user_duty import DingtalkDeptUserDutyEntity
from infra_dingtalk.model.dingtalk_dept_user_duty_model import DingtalkDeptUserDutyModel


class DingtalkDeptUserDutyRepository(BasicRepository):
    """
    钉钉部门用户职责
    """

    def insert_dingtalk_dept_user_duty(
        self, data: DingtalkDeptUserDutyModel, transaction: Transaction
    ) -> str:
        """
        插入钉钉部门用户职责
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkDeptUserDutyEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_dingtalk_dept_user_duty(
        self, data: DingtalkDeptUserDutyModel, transaction: Transaction
    ):
        """
        更新钉钉部门用户职责
        只会更新职责这个字段，若部门有变化，那条数据应该被删除
        所以col_list写死为["duty"]
        """
        self._update_versioned_entity_by_model(
            entity_cls=DingtalkDeptUserDutyEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=["duty"],
        )

    def delete_dingtalk_dept_user_duty(
        self, dingtalk_dept_user_duty_id: str, transaction: Transaction
    ):
        """
        删除钉钉部门用户职责
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkDeptUserDutyEntity,
            entity_id=dingtalk_dept_user_duty_id,
            transaction=transaction,
        )

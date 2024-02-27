"""
钉钉用户k12的部门职责
"""

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_user_k12_dept_duty import DingtalkUserK12DeptDutyEntity
from infra_dingtalk.model.dingtalk_user_k12_dept_duty_model import DingtalkUserK12DeptDutyModel
from infra_dingtalk.model.view.dingtalk_dept_user_duty_vm import DingtalkDeptUserDutyVm


class DingtalkUserK12DeptDutyRepository(BasicRepository):
    """
    钉钉用户k12的部门职责
    """

    def insert_dingtalk_user_k12_dept_duty(
        self, data: DingtalkUserK12DeptDutyModel, transaction: Transaction
    ) -> str:
        """
        插入钉钉用户在k12部门中的职责
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkUserK12DeptDutyEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_dingtalk_user_k12_dept_duty(
        self, data: DingtalkUserK12DeptDutyModel, transaction: Transaction
    ):
        """
        更新钉钉用户在k12部门中的职责
        """
        self._update_versioned_entity_by_model(
            entity_cls=DingtalkUserK12DeptDutyEntity,
            update_model=data,
            transaction=transaction,
        )

    def delete_dingtalk_user_k12_dept_duty(self, dept_duty_id: str, transaction: Transaction):
        """
        删除钉钉用户在k12部门中的职责
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkUserK12DeptDutyEntity,
            entity_id=dept_duty_id,
            transaction=transaction,
        )

    def get_dingtalk_user_distinct_dept_duty_list(self, dingtalk_user_id: str):
        """
        获取user不同的k12_dept_duty
        """
        sql = """
        select distinct dingtalk_user_id, duty from
        st_dingtalk_user_k12_dept_duty where dingtalk_user_id = :dingtalk_user_id
        """
        return self._fetch_all_to_model(
            sql=sql, model_cls=DingtalkDeptUserDutyVm, params={"dingtalk_user_id": dingtalk_user_id}
        )

"""
同步用户的服务
"""
import logging
from typing import Dict

from infra_basic.transaction import Transaction

from infra_dingtalk.data.agent_plugin.dingtalk_user import DingtalkUser
from infra_dingtalk.model.dingtalk_dept_model import DingtalkDeptModel
from infra_dingtalk.model.dingtalk_dept_user_duty_model import DingtalkDeptUserDutyModel
from infra_dingtalk.model.dingtalk_user_model import DingtalkUserModel
from infra_dingtalk.repository.dingtalk_dept_user_duty_repository import (
    DingtalkDeptUserDutyRepository,
)
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository


class SyncUserService:
    def __init__(
        self,
        dingtalk_user_repository: DingtalkUserRepository,
        dingtalk_dept_user_duty_repository: DingtalkDeptUserDutyRepository,
    ):
        self._dingtalk_user_repository = dingtalk_user_repository
        self._dingtalk_dept_user_duty_repository = dingtalk_dept_user_duty_repository

    def sync_dingtalk_user_from_remote(
        self,
        remote_user_dict: Dict[str, DingtalkUser],
        db_dept_dict: Dict[int, DingtalkDeptModel],
        dingtalk_corp_id: str,
        transaction: Transaction,
    ):
        """
        远程的用户和数据库的用户进行比较
        """
        db_user_dict = self.get_dingtalk_user_remote_id_dict(dingtalk_corp_id=dingtalk_corp_id)

        for remote_user_id, remote_user in remote_user_dict.items():
            db_user = db_user_dict.get(remote_user_id)
            if not db_user:
                new_db_user = self.add_dingtalk_user(
                    remote_user=remote_user,
                    dingtalk_corp_id=dingtalk_corp_id,
                    db_dept_dict=db_dept_dict,
                    transaction=transaction,
                )
                db_user_dict[remote_user_id] = new_db_user
            else:
                self.update_dingtalk_user(
                    remote_user=remote_user,
                    db_user=db_user,
                    db_dept_dict=db_dept_dict,
                    transaction=transaction,
                )
        for db_remote_user_id, db_user in db_user_dict.items():
            if db_remote_user_id not in remote_user_dict:
                self._dingtalk_user_repository.delete_dingtalk_user(
                    dingtalk_user_id=db_user.id, transaction=transaction
                )

    def get_dingtalk_user_remote_id_dict(
        self,
        dingtalk_corp_id: str,
    ) -> Dict[str, DingtalkUserModel]:
        """
        获取钉钉用户以远程id为键的字典
        """
        db_user_list = self._dingtalk_user_repository.fetch_dingtalk_user_list_with_dept(
            dingtalk_corp_id=dingtalk_corp_id
        )
        return {x.remote_user_id: x for x in db_user_list}

    def add_dingtalk_user(
        self,
        remote_user: DingtalkUser,
        dingtalk_corp_id: str,
        db_dept_dict: Dict[int, DingtalkDeptModel],
        transaction: Transaction,
    ) -> DingtalkUserModel:
        """
        添加钉钉用户
        """
        new_user = remote_user.to_dingtalk_user_em(
            dingtalk_corp_id=dingtalk_corp_id,
        )
        new_user.id = self._dingtalk_user_repository.insert_dingtalk_user(
            user=new_user, transaction=transaction
        )
        for remote_dept_id in remote_user.department:
            dept = db_dept_dict.get(remote_dept_id)
            if not dept:
                logging.error(f"同步用户{remote_user.userid}时发现id为{remote_dept_id}的部门未同步")
                continue
            self._dingtalk_dept_user_duty_repository.insert_dingtalk_dept_user_duty(
                data=DingtalkDeptUserDutyModel(
                    dingtalk_user_id=new_user.id,
                    dingtalk_dept_id=dept.id,
                    duty=remote_user.get_dept_duty(remote_dept_id),
                ),
                transaction=transaction,
            )
        return new_user

    def update_dingtalk_user(
        self,
        remote_user: DingtalkUser,
        db_user: DingtalkUserModel,
        db_dept_dict: Dict[int, DingtalkDeptModel],
        transaction: Transaction,
    ):
        """
        更新钉钉用户信息
        """
        remote_unique_dict = remote_user.unique_dict()
        if remote_unique_dict != db_user.unique_dict():
            new_db_user = db_user.cast_to(
                cast_type=DingtalkUserModel,
                **remote_user.dict(),
            )
            new_db_user.empty_to_none()
            self._dingtalk_user_repository.update_dingtalk_user(
                user=new_db_user, transaction=transaction
            )
        for remote_dept_id in remote_user.department:
            duty = remote_user.get_dept_duty(remote_dept_id)
            if remote_dept_id not in db_user.remote_dept_ids:
                dept = db_dept_dict.get(remote_dept_id)
                if not dept:
                    logging.error(f"同步用户{remote_user.userid}时发现id为{remote_dept_id}的部门未同步")
                    continue
                self._dingtalk_dept_user_duty_repository.insert_dingtalk_dept_user_duty(
                    data=DingtalkDeptUserDutyModel(
                        dingtalk_user_id=db_user.id, dingtalk_dept_id=dept.id, duty=duty
                    ),
                    transaction=transaction,
                )
                continue
            for db_dept_duty in db_user.dingtalk_dept_user_duty_list:
                if db_dept_duty.remote_dept_id == remote_dept_id and duty != db_dept_duty.duty:
                    self._dingtalk_dept_user_duty_repository.update_dingtalk_dept_user_duty(
                        data=db_dept_duty.cast_to(cast_type=DingtalkDeptUserDutyModel, duty=duty),
                        transaction=transaction,
                    )
        for db_dept_duty in db_user.dingtalk_dept_user_duty_list:
            if db_dept_duty.remote_dept_id not in remote_user.department:
                self._dingtalk_dept_user_duty_repository.delete_dingtalk_dept_user_duty(
                    dingtalk_dept_user_duty_id=db_dept_duty.id,
                    transaction=transaction,
                )

import logging
from typing import Dict, Optional

from infra_basic.errors.input import DataNotFoundError
from infra_basic.transaction import Transaction

from infra_dingtalk.data.agent_plugin.dingtalk_k12_dept import DingtalkK12Dept
from infra_dingtalk.model.dingtalk_user_k12_dept_duty_model import DingtalkUserK12DeptDutyModel
from infra_dingtalk.model.view.dingtalk_k12_dept_with_admins_vm import (
    DingtalkK12DeptWithAdminsViewModel,
)
from infra_dingtalk.repository.dingtalk_k12_dept_repository import DingtalkK12DeptRepository
from infra_dingtalk.repository.dingtalk_user_k12_dept_duty_repository import (
    DingtalkUserK12DeptDutyRepository,
)
from infra_dingtalk.service.sync_user_service import SyncUserService


class K12SyncDeptService:
    """
    同步k12部门
    """

    def __init__(
        self,
        sync_user_service: SyncUserService,
        dingtalk_k12_dept_repository: DingtalkK12DeptRepository,
        dingtalk_user_k12_dept_duty_repository: DingtalkUserK12DeptDutyRepository,
    ):
        self._sync_user_service = sync_user_service
        self._dingtalk_k12_dept_repository = dingtalk_k12_dept_repository
        self._dingtalk_user_k12_dept_duty_repository = dingtalk_user_k12_dept_duty_repository

        # 为了最小的改动
        self._dingtalk_corp_id = None
        self._remote_dept_dict = None
        self._transaction = None
        self._db_k12_dept_dict = None
        self._db_user_dict = None

    def super_init_attr(
        self,
        dingtalk_corp_id: str,
        remote_dept_dict: Dict[int, DingtalkK12Dept],
        transaction: Transaction,
    ):
        self._dingtalk_corp_id = dingtalk_corp_id
        self._remote_dept_dict = remote_dept_dict
        self._transaction = transaction
        self._db_k12_dept_dict = self.get_db_k12_dept_dict()
        self._db_user_dict = self._sync_user_service.get_dingtalk_user_remote_id_dict(
            dingtalk_corp_id=dingtalk_corp_id
        )

    def get_db_k12_dept_dict(
        self,
    ) -> Dict[int, DingtalkK12DeptWithAdminsViewModel]:
        """
        获取k12部门以远程id未键的字典
        """
        db_k12_dept_list = self._dingtalk_k12_dept_repository.fetch_dingtalk_k12_dept_with_admins(
            dingtalk_corp_id=self._dingtalk_corp_id
        )
        return {x.remote_dept_id: x for x in db_k12_dept_list}

    def __get_db_parent_k12_dept_id(self, parent_remote_dept_id: int) -> Optional[str]:
        """
        获取部门在数据库中的id
        """
        if parent_remote_dept_id != 0:
            _parent = self._db_k12_dept_dict.get(parent_remote_dept_id)
            if not _parent:
                raise DataNotFoundError(f"{parent_remote_dept_id}的部门")
            return _parent.id
        return None

    def sync_remote_k12_dept_to_db(
        self,
        dingtalk_corp_id: str,
        remote_dept_dict: Dict[int, DingtalkK12Dept],
        transaction: Transaction,
    ) -> Dict[int, DingtalkK12DeptWithAdminsViewModel]:
        """
        从API获取到的k12部门和数据库的部门进行比较并进行同步
        """
        self.super_init_attr(
            dingtalk_corp_id=dingtalk_corp_id,
            remote_dept_dict=remote_dept_dict,
            transaction=transaction,
        )
        for remote_dept_id, remote_dept in self._remote_dept_dict.items():
            db_dept = self._db_k12_dept_dict.get(remote_dept_id)
            if not db_dept:
                self.__add_dingtalk_k12_dept(remote_dept=remote_dept)
            else:
                self.__update_dingtalk_k12_dept(remote_dept=remote_dept, db_dept=db_dept)
                self.__update_dingtalk_k12_admin(remote_dept=remote_dept, db_dept=db_dept)
        for db_remote_dept_id, db_dept in self._db_k12_dept_dict.items():
            if db_remote_dept_id not in self._remote_dept_dict:
                self.__delete_dingtalk_k12_dept(db_dept=db_dept)
        return self._db_k12_dept_dict

    def __add_dingtalk_k12_dept(self, remote_dept: DingtalkK12Dept):
        """
        添加企业微信的k12部门
        """

        db_k12_dept = remote_dept.to_dingtalk_k12_dept_em(
            dingtalk_corp_id=self._dingtalk_corp_id,
            parent_dingtalk_dept_id=self.__get_db_parent_k12_dept_id(
                parent_remote_dept_id=remote_dept.parent_id
            ),
            parent_remote_dept_id=remote_dept.parent_id,
        )
        db_k12_dept.id = self._dingtalk_k12_dept_repository.insert_dingtalk_k12_dept(
            dept=db_k12_dept, transaction=self._transaction
        )
        self._db_k12_dept_dict[remote_dept.dept_id] = db_k12_dept.cast_to(
            cast_type=DingtalkK12DeptWithAdminsViewModel
        )

    def __update_dingtalk_k12_dept(
        self,
        remote_dept: DingtalkK12Dept,
        db_dept: DingtalkK12DeptWithAdminsViewModel,
    ):
        """
        更新企业微信k12的部门
        """
        if remote_dept.unique_dict() != db_dept.unique_dict():
            new_db_k12_dept = remote_dept.to_dingtalk_k12_dept_em(
                dingtalk_corp_id=self._dingtalk_corp_id,
                parent_dingtalk_dept_id=self.__get_db_parent_k12_dept_id(
                    parent_remote_dept_id=remote_dept.parent_id
                ),
                parent_remote_dept_id=remote_dept.parent_id,
            )
            new_db_k12_dept.id = db_dept.id
            new_db_k12_dept.version = db_dept.version
            self._dingtalk_k12_dept_repository.update_dingtalk_k12_dept(
                dept=new_db_k12_dept, transaction=self._transaction
            )

    def __update_dingtalk_k12_admin(
        self,
        remote_dept: DingtalkK12Dept,
        db_dept: DingtalkK12DeptWithAdminsViewModel,
    ):
        """
        更新k12部门的负责人
        """
        for remote_admin in remote_dept.department_admins:
            existed = False
            for db_admin in db_dept.admins:
                if (
                    remote_admin.userid == db_admin.remote_user_id
                    and remote_admin.duty == db_admin.duty
                ):
                    existed = True
                    if remote_admin.subject != db_admin.subject:
                        db_admin.subject = remote_admin.subject
                        self._dingtalk_user_k12_dept_duty_repository.update_dingtalk_user_k12_dept_duty(
                            data=db_admin.cast_to(cast_type=DingtalkUserK12DeptDutyModel),
                            transaction=self._transaction,
                        )
            if not existed:
                dingtalk_user = self._db_user_dict.get(remote_admin.userid)
                if not dingtalk_user:
                    logging.info(f"未找到id为【{remote_admin.userid}】的用户")
                    continue
                self._dingtalk_user_k12_dept_duty_repository.insert_dingtalk_user_k12_dept_duty(
                    data=remote_admin.to_dingtalk_user_k12_dept_duty_em(
                        dingtalk_user_id=dingtalk_user.id,
                        dingtalk_k12_dept_id=db_dept.id,
                    ),
                    transaction=self._transaction,
                )
        for db_admin in db_dept.admins:
            existed = False
            for remote_admin in remote_dept.department_admins:
                if (
                    remote_admin.userid == db_admin.remote_user_id
                    and remote_admin.duty == db_admin.duty
                ):
                    existed = True
            if not existed:
                self._dingtalk_user_k12_dept_duty_repository.delete_dingtalk_user_k12_dept_duty(
                    dept_duty_id=db_admin.id, transaction=self._transaction
                )

    def __delete_dingtalk_k12_dept(self, db_dept: DingtalkK12DeptWithAdminsViewModel):
        """
        删除企业微信的k12部门
        """
        self._dingtalk_k12_dept_repository.delete_dingtalk_k12_dept(
            dept_id=db_dept.id, transaction=self._transaction
        )
        for admin in db_dept.admins:
            self._dingtalk_user_k12_dept_duty_repository.delete_dingtalk_user_k12_dept_duty(
                dept_duty_id=admin.id, transaction=self._transaction
            )

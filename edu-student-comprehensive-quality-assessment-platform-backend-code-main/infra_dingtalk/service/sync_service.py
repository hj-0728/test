from infra_basic.transaction import Transaction

from infra_dingtalk.data.agent_plugin.dingtalk_student import DingtalkStudent
from infra_dingtalk.model.dingtalk_k12_dept_model import EnumDingtalkK12DeptType
from infra_dingtalk.service.plugin_service import PluginService
from infra_dingtalk.service.sync_dept_service import SyncDeptService
from infra_dingtalk.service.sync_k12_dept_service import K12SyncDeptService
from infra_dingtalk.service.sync_k12_student_service import K12SyncStudentService
from infra_dingtalk.service.sync_user_service import SyncUserService


class SyncService:
    """
    同步服务
    """

    def __init__(
        self,
        plugin_service: PluginService,
        sync_user_service: SyncUserService,
        sync_dept_service: SyncDeptService,
        sync_k12_dept_service: K12SyncDeptService,
        sync_k12_student_service: K12SyncStudentService,
    ):
        self._plugin_service = plugin_service
        self._sync_user_service = sync_user_service
        self._sync_dept_service = sync_dept_service
        self._sync_k12_dept_service = sync_k12_dept_service
        self._sync_k12_student_service = sync_k12_student_service

    def sync_inner_from_remote(self, dingtalk_corp_id: str, transaction: Transaction):
        """
        从远程开始同步
        同步企业内部用户、部门
        """
        plugin = self._plugin_service.get_sync_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        remote_dept_dict = plugin.get_all_dd_dept()
        db_dept_dict = self._sync_dept_service.sync_dingtalk_dept_from_remote(
            remote_dept_dict=remote_dept_dict,
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=transaction,
        )
        remote_user_dict = plugin.get_dd_user_list(remote_dept_ids=list(remote_dept_dict.keys()))
        self._sync_user_service.sync_dingtalk_user_from_remote(
            remote_user_dict=remote_user_dict,
            db_dept_dict=db_dept_dict,
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=transaction,
        )

    def sync_k12_from_remote(self, dingtalk_corp_id: str, transaction: Transaction):
        """
        从远程开始同步
        同步k12的用户、部门
        """
        plugin = self._plugin_service.get_k12_sync_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        remote_dept_dict = plugin.get_all_dept()
        db_k12_dept_dict = self._sync_k12_dept_service.sync_remote_k12_dept_to_db(
            dingtalk_corp_id=dingtalk_corp_id,
            remote_dept_dict=remote_dept_dict,
            transaction=transaction,
        )
        student_list = []
        for k12_dept in remote_dept_dict.values():
            if k12_dept.dept_type == EnumDingtalkK12DeptType.CLASS.name.lower():
                student_list += plugin.get_k12_student(class_id=k12_dept.dept_id)
        remote_student_dict = {}
        for student in student_list:
            student["department"] = [student["class_id"]]
            if remote_student_dict.get(student["userid"]):
                remote_student_dict[student["userid"]].department.append(student["class_id"])
            else:
                remote_student_dict[student["userid"]] = DingtalkStudent(**student)
        self._sync_k12_student_service.sync_remote_parent_to_db(
            dingtalk_corp_id=dingtalk_corp_id,
            remote_student_dict=remote_student_dict,
            db_k12_dept_dict=db_k12_dept_dict,
            transaction=transaction,
        )
        self._sync_k12_student_service.sync_remote_student_to_db()

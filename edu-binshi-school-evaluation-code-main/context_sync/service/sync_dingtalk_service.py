from infra_basic.transaction import Transaction

from context_sync.model.context_organization_corp_map_model import EnumContextOrgCorpMapResCategory
from context_sync.repository.context_dept_map_repository import ContextDeptMapRepository
from context_sync.repository.context_organization_corp_map_repository import (
    ContextOrganizationCorpMapRepository,
)
from context_sync.service.sync_dingtalk_dept_service import SyncDingtalkDeptService
from context_sync.service.sync_dingtalk_user_service import SyncDingtalkUserService


class SyncDingtalkService:
    def __init__(
        self,
        sync_dingtalk_dept_service: SyncDingtalkDeptService,
        sync_dingtalk_user_service: SyncDingtalkUserService,
        context_org_corp_map_repository: ContextOrganizationCorpMapRepository,
        context_dept_map_repository: ContextDeptMapRepository,
    ):
        self.__sync_dingtalk_user_service = sync_dingtalk_user_service
        self.__sync_dingtalk_dept_service = sync_dingtalk_dept_service
        self.__context_org_corp_map_repository = context_org_corp_map_repository
        self.__context_dept_map_repository = context_dept_map_repository

    def sync_dingtalk_dept_to_master(self, dingtalk_corp_id: str, transaction: Transaction):
        """
        同步部门
        """
        context_org_corp_map = (
            self.__context_org_corp_map_repository.fetch_context_org_corp_map_by_res(
                res_category=EnumContextOrgCorpMapResCategory.DINGTALK.name, res_id=dingtalk_corp_id
            )
        )
        # 同步k12部门
        self.__sync_dingtalk_dept_service.sync_dingtalk_edu_contacts_dept(
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=transaction,
            organization_id=context_org_corp_map.organization_id,
        )
        # 同步内部部门
        self.__sync_dingtalk_dept_service.sync_dingtalk_contacts_dept(
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=transaction,
            organization_id=context_org_corp_map.organization_id,
        )

    def sync_dingtalk_user_to_master(self, dingtalk_corp_id: str, transaction: Transaction):
        """
        同步钉钉用户到 master
        """
        context_org_corp_map = (
            self.__context_org_corp_map_repository.fetch_context_org_corp_map_by_res(
                res_category=EnumContextOrgCorpMapResCategory.DINGTALK.name, res_id=dingtalk_corp_id
            )
        )
        context_dept_list = (
            self.__context_dept_map_repository.get_context_dept_detail_by_res_category(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )
        contest_k12_dept_list = (
            self.__context_dept_map_repository.get_context_k12_dept_detail_by_res_category(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )
        self.__sync_dingtalk_user_service.sync_dingtalk_inner_people(
            dingtalk_corp_id=dingtalk_corp_id,
            context_dept_map={x.res_dept_id: x.dimension_dept_tree_id for x in context_dept_list},
            context_k12_dept_map={
                x.res_dept_id: x.dimension_dept_tree_id for x in contest_k12_dept_list
            },
            organization_id=context_org_corp_map.organization_id,
            transaction=transaction,
        )

    def sync_dingtalk_parent_and_student_to_master(
        self, dingtalk_corp_id: str, transaction: Transaction
    ):
        """
        同步钉钉用户到 master
        """
        context_org_corp_map = (
            self.__context_org_corp_map_repository.fetch_context_org_corp_map_by_res(
                res_category=EnumContextOrgCorpMapResCategory.DINGTALK.name, res_id=dingtalk_corp_id
            )
        )
        contest_k12_dept_list = (
            self.__context_dept_map_repository.get_context_k12_dept_detail_by_res_category(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )
        self.__sync_dingtalk_user_service.sync_dingtalk_parent_and_student(
            dingtalk_corp_id=dingtalk_corp_id,
            context_dept_map={
                x.res_dept_id: x.dimension_dept_tree_id for x in contest_k12_dept_list
            },
            organization_id=context_org_corp_map.organization_id,
            transaction=transaction,
        )

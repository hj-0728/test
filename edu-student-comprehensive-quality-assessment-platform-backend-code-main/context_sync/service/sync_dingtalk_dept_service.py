import random
from typing import Dict, List

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.enum_helper import get_enum_value_by_name
from infra_utility.token_helper import generate_uuid_id

from biz_comprehensive.data.enum import EnumDictMetaCode
from context_sync.model.context_dept_map_model import (
    ContextDeptMapModel,
    EnumContextDeptMapResCategory,
)
from context_sync.model.view.context_dept_detail_vm import ContextDeptDetailViewModel
from context_sync.repository.context_dept_map_repository import ContextDeptMapRepository
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.dept_model import DeptModel
from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.edit.add_dept_dept_category_map_em import AddDeptDeptCategoryMapEditModel
from infra_backbone.model.edit.add_dept_em import AddDeptEditModel
from infra_backbone.repository.dict_repository import DictRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.service.dept_dept_category_map_service import DeptDeptCategoryMapService
from infra_backbone.service.dept_service import DeptService
from infra_dingtalk.model.dingtalk_dept_model import DingtalkDeptModel
from infra_dingtalk.model.dingtalk_k12_dept_model import (
    DingtalkK12DeptModel,
    EnumDingtalkK12DeptType,
)
from infra_dingtalk.repository.dingtalk_dept_repository import DingtalkDeptRepository
from infra_dingtalk.repository.dingtalk_k12_dept_repository import DingtalkK12DeptRepository


class SyncDingtalkDeptService:
    def __init__(
        self,
        dingtalk_k12_dept_repository: DingtalkK12DeptRepository,
        context_dept_map_repository: ContextDeptMapRepository,
        dept_service: DeptService,
        dept_dept_category_map_service: DeptDeptCategoryMapService,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        dingtalk_dept_repository: DingtalkDeptRepository,
        object_storage_service: ObjectStorageService,
        dict_repository: DictRepository,
    ):
        self.__dingtalk_k12_dept_repository = dingtalk_k12_dept_repository
        self.__context_dept_map_repository = context_dept_map_repository
        self.__dept_service = dept_service
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__dept_dept_category_map_service = dept_dept_category_map_service
        self.__dingtalk_dept_repository = dingtalk_dept_repository
        self.__object_storage_service = object_storage_service
        self.__dict_repository = dict_repository

    def sync_dingtalk_edu_contacts_dept(
        self, dingtalk_corp_id: str, organization_id: str, transaction: Transaction
    ) -> Dict[str, str]:
        """
        同步家校通讯录部门
        :param dingtalk_corp_id:
        :param organization_id:
        :param transaction:
        :return:
        """

        k12_dept_list = self.__dingtalk_k12_dept_repository.get_dingtalk_k12_dept_by_corp_id(
            dingtalk_corp_id=dingtalk_corp_id
        )

        context_dept_detail_list = (
            self.__context_dept_map_repository.get_context_k12_dept_detail_by_res_category(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )

        k12_dept_id_list = [x.id for x in k12_dept_list]
        context_res_dept_id_list = [x.res_dept_id for x in context_dept_detail_list]

        # 不在 k12 删除，部门删除

        self.__remove_dept(
            dept_id_list=k12_dept_id_list,
            context_dept_detail_list=context_dept_detail_list,
            transaction=transaction,
        )

        # 在 k12 ，不在 上下文，添加

        add_context_dept_map = self.__add_k12_dept(
            k12_dept_list=k12_dept_list,
            context_res_dept_id_list=context_res_dept_id_list,
            organization_id=organization_id,
            transaction=transaction,
        )

        # 在 k12 ，在 上下文，判断是否需要修改

        context_dept_map = {x.res_dept_id: x.dept_id for x in context_dept_detail_list}

        context_dept_map |= add_context_dept_map

        self.__update_k12_dept(
            k12_dept_list=k12_dept_list,
            context_dept_detail_list=context_dept_detail_list,
            context_dept_map=context_dept_map,
            transaction=transaction,
        )

        return context_dept_map

    def sync_dingtalk_contacts_dept(
        self, dingtalk_corp_id: str, organization_id: str, transaction: Transaction
    ) -> Dict[str, str]:
        """
        同步内部通讯录部门
        :param dingtalk_corp_id:
        :param organization_id:
        :param transaction:
        :return:
        """

        dept_list = self.__dingtalk_dept_repository.get_dingtalk_dept_by_corp_id(
            dingtalk_corp_id=dingtalk_corp_id
        )

        context_dept_detail_list = (
            self.__context_dept_map_repository.get_context_dept_detail_by_res_category(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )

        dept_id_list = [x.id for x in dept_list]
        context_res_dept_id_list = [x.res_dept_id for x in context_dept_detail_list]

        # 添加部门

        add_context_dept_map = self.__add_dept(
            dept_list=dept_list,
            context_res_dept_id_list=context_res_dept_id_list,
            organization_id=organization_id,
            transaction=transaction,
        )

        # 在 k12 ，在 上下文，判断是否需要修改

        context_dept_map = {x.res_dept_id: x.dept_id for x in context_dept_detail_list}

        context_dept_map |= add_context_dept_map

        self.__update_dept(
            dept_list=dept_list,
            context_dept_detail_list=context_dept_detail_list,
            context_dept_map=context_dept_map,
            transaction=transaction,
        )

        # 删除部门
        self.__remove_dept(
            dept_id_list=dept_id_list,
            context_dept_detail_list=context_dept_detail_list,
            transaction=transaction,
        )

        return context_dept_map

    def __remove_dept(
        self,
        dept_id_list: List[str],
        context_dept_detail_list: List[ContextDeptDetailViewModel],
        transaction: Transaction,
    ):
        """
        移除需要删除的部门
        :param dept_id_list:
        :param context_dept_detail_list:
        :param transaction:
        :return:
        """

        for context_dept_detail in context_dept_detail_list:
            if context_dept_detail.res_dept_id not in dept_id_list:
                self.__dept_service.delete_dept(
                    dept_id=context_dept_detail.dept_id,
                    transaction=transaction,
                )
                self.__dimension_dept_tree_repository.delete_dimension_dept_tree(
                    tree_id=context_dept_detail.dimension_dept_tree_id,
                    transaction=transaction,
                )
                self.__context_dept_map_repository.delete_context_dept_map(
                    context_dept_map_id=context_dept_detail.id, transaction=transaction
                )

    def __add_k12_dept(
        self,
        k12_dept_list: List[DingtalkK12DeptModel],
        context_res_dept_id_list: List[str],
        organization_id: str,
        transaction: Transaction,
    ) -> Dict[str, str]:
        """
        添加k12部门
        :param k12_dept_list:
        :param context_res_dept_id_list:
        :param organization_id:
        :param transaction:
        :return:
        """

        need_add_dept_dict = {}
        class_ids = []

        for k12_dept in k12_dept_list:
            if k12_dept.id not in context_res_dept_id_list:
                data = AddDeptEditModel(
                    id=generate_uuid_id(),
                    dimension_category=EnumDimensionCategory.EDU.name,
                    organization_id=organization_id,
                    name=k12_dept.name,
                    parent_dept_id=k12_dept.parent_dingtalk_k12_dept_id,
                    category_code=k12_dept.dept_type,
                    seq=k12_dept.remote_dept_id,
                )
                need_add_dept_dict[k12_dept.id] = data

                # 给k12的班级加上头像
                if k12_dept.dept_type == EnumDingtalkK12DeptType.CLASS.name:
                    class_ids.append(data.id)

        context_dept_map = {}
        for k12_dept_id, dept_em in need_add_dept_dict.items():
            if dept_em.parent_dept_id and need_add_dept_dict.get(dept_em.parent_dept_id):
                dept_em.parent_dept_id = need_add_dept_dict.get(dept_em.parent_dept_id).id

            self.__dept_service.add_dept_info(data=dept_em, transaction=transaction)
            self.__context_dept_map_repository.insert_context_dept_map(
                context_dept_map=ContextDeptMapModel(
                    dept_id=dept_em.id,
                    res_category=EnumContextDeptMapResCategory.DINGTALK_K12_DEPT.name,
                    res_id=k12_dept_id,
                ),
                transaction=transaction,
            )
            context_dept_map[k12_dept_id] = dept_em.id

        self.add_dept_default_avatar(dept_ids=class_ids, transaction=transaction)

        return context_dept_map

    def __add_dept(
        self,
        dept_list: List[DingtalkDeptModel],
        context_res_dept_id_list: List[str],
        organization_id: str,
        transaction: Transaction,
    ) -> Dict[str, str]:
        """

        :param dept_list:
        :param context_res_dept_id_list:
        :param organization_id:
        :param transaction:
        :return:
        """

        need_add_dept_dict = {}

        for dept in dept_list:
            if dept.id not in context_res_dept_id_list:
                data = AddDeptEditModel(
                    id=generate_uuid_id(),
                    dimension_category=EnumDimensionCategory.ADMINISTRATION.name,
                    organization_id=organization_id,
                    name=dept.name,
                    parent_dept_id=dept.parent_dingtalk_dept_id,
                    seq=dept.seq,
                )
                need_add_dept_dict[dept.id] = data
        context_dept_map = {}
        for dept_id, dept_em in need_add_dept_dict.items():
            if dept_em.parent_dept_id and need_add_dept_dict.get(dept_em.parent_dept_id):
                dept_em.parent_dept_id = need_add_dept_dict.get(dept_em.parent_dept_id).id

            self.__dept_service.add_dept_info(data=dept_em, transaction=transaction)
            self.__context_dept_map_repository.insert_context_dept_map(
                context_dept_map=ContextDeptMapModel(
                    dept_id=dept_em.id,
                    res_category=EnumContextDeptMapResCategory.DINGTALK_DEPT.name,
                    res_id=dept_id,
                ),
                transaction=transaction,
            )
            context_dept_map[dept_id] = dept_em.id

        return context_dept_map

    def __update_k12_dept(
        self,
        k12_dept_list: List[DingtalkK12DeptModel],
        context_dept_detail_list: List[ContextDeptDetailViewModel],
        context_dept_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        修改k12部门
        :param k12_dept_list:
        :param context_dept_detail_list:
        :param context_dept_map:
        :param transaction:
        :return:
        """

        k12_dept_dict = {x.id: x for x in k12_dept_list}

        for dept in context_dept_detail_list:
            k12_dept = k12_dept_dict.get(dept.res_dept_id)
            if k12_dept:
                if dept.name != k12_dept.name:
                    self.__dept_service.update_dept(
                        dept_info=DeptModel(
                            id=dept.dept_id,
                            version=dept.dept_version,
                            name=k12_dept.name,
                            organization_id=dept.organization_id,
                        ),
                        transaction=transaction,
                        limited_col_list=["name"],
                    )
                dd_parent_id = k12_dept.parent_dingtalk_k12_dept_id
                if dd_parent_id and context_dept_map.get(dd_parent_id) != dept.parent_dept_id:
                    self.__dimension_dept_tree_repository.update_dimension_dept_tree(
                        data=DimensionDeptTreeModel(
                            id=dept.dimension_dept_tree_id,
                            version=dept.dimension_dept_tree_version,
                            dept_id=dept.id,
                            parent_dept_id=context_dept_map.get(dd_parent_id),
                            seq=k12_dept.remote_dept_id,
                        ),
                        transaction=transaction,
                        limited_col_list=["parent_dept_id", "seq"],
                    )

                if k12_dept.dept_type not in dept.category_code_list:
                    self.__dept_dept_category_map_service.add_dept_dept_category_map(
                        dept_dept_category_map_data=AddDeptDeptCategoryMapEditModel(
                            dept_id=dept.id,
                            organization_id=dept.organization_id,
                            category_code=k12_dept.dept_type,
                            category_name=get_enum_value_by_name(
                                enum_class=EnumDingtalkK12DeptType,
                                enum_name=k12_dept.dept_type,
                            ),
                        ),
                        transaction=transaction,
                    )

    def __update_dept(
        self,
        dept_list: List[DingtalkDeptModel],
        context_dept_detail_list: List[ContextDeptDetailViewModel],
        context_dept_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        修改部门
        :param dept_list:
        :param context_dept_detail_list:
        :param context_dept_map:
        :param transaction:
        :return:
        """

        dept_dict = {x.id: x for x in dept_list}

        for context_dept in context_dept_detail_list:
            dept = dept_dict.get(context_dept.res_dept_id)
            if dept:
                if context_dept.name != dept.name:
                    self.__dept_service.update_dept(
                        dept_info=DeptModel(
                            id=context_dept.dept_id,
                            version=context_dept.dept_version,
                            name=dept.name,
                            organization_id=context_dept.organization_id,
                        ),
                        transaction=transaction,
                        limited_col_list=["name"],
                    )
                dd_parent_id = dept.parent_dingtalk_dept_id
                if (
                    dd_parent_id
                    and context_dept_map.get(dd_parent_id) != context_dept.parent_dept_id
                ):
                    self.__dimension_dept_tree_repository.update_dimension_dept_tree(
                        data=DimensionDeptTreeModel(
                            id=context_dept.dimension_dept_tree_id,
                            version=context_dept.dimension_dept_tree_version,
                            dept_id=context_dept.id,
                            parent_dept_id=context_dept_map.get(dd_parent_id),
                            seq=dept.seq,
                        ),
                        transaction=transaction,
                        limited_col_list=["parent_dept_id", "seq"],
                    )

    def add_dept_default_avatar(self, dept_ids: List[str], transaction: Transaction):
        """
        添加部门默认头像
        :return:
        """
        avatar_list = self.__dict_repository.get_dict_data_by_meta_code(
            dict_meta_code=EnumDictMetaCode.DEPT_DEFAULT_AVATAR.name
        )
        for dept_id in dept_ids:
            seq = random.randint(0, len(avatar_list) - 1)
            avatar_file_id = avatar_list[seq].value
            self.__object_storage_service.link_file_and_resource(
                file_id=avatar_file_id,
                resource=BasicResource(id=dept_id, category=EnumBackboneResource.DEPT.name),
                relationship=EnumFileRelationship.AVATAR.name,
                transaction=transaction,
            )

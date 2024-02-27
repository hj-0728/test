from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree, TreeNodeModel
from infra_utility.token_helper import generate_uuid_id

from infra_backbone.model.ability_permission_assign_model import (
    AbilityPermissionAssignTreeViewModel,
)
from infra_backbone.model.ability_permission_tree_model import (
    AbilityPermissionTreeModel,
    EnumChildResourceCategory,
)
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel
from infra_backbone.model.edit.granted_ability_permission_em import AbilityPermissionAssignEm
from infra_backbone.model.view.ability_permission_vm import AbilityPermissionTreeViewModel
from infra_backbone.repository.ability_permission_assign_repository import (
    AbilityPermissionAssignRepository,
)
from infra_backbone.repository.ability_permission_group_repository import (
    AbilityPermissionGroupRepository,
)
from infra_backbone.repository.ability_permission_repository import AbilityPermissionRepository
from infra_backbone.repository.ability_permission_tree_repository import (
    AbilityPermissionTreeRepository,
)


class AbilityPermissionService:
    def __init__(
        self,
        ability_permission_repository: AbilityPermissionRepository,
        ability_permission_group_repository: AbilityPermissionGroupRepository,
        ability_permission_tree_repository: AbilityPermissionTreeRepository,
        ability_permission_assign_repository: AbilityPermissionAssignRepository,
    ):
        self.__ability_permission_repository = ability_permission_repository
        self.__ability_permission_group_repository = ability_permission_group_repository
        self.__ability_permission_tree_repository = ability_permission_tree_repository
        self.__ability_permission_assign_repository = ability_permission_assign_repository

    def create_ability_permission(
        self,
        ability_permission_em: AbilityPermissionEditModel,
        transaction: Transaction,
    ) -> str:
        """
        创建功能权限
        :param ability_permission_em:
        :param transaction:
        :return:
        """

        ability_permission_em.id = generate_uuid_id()
        if ability_permission_em.is_permission:
            self.check_ability_permission(
                name=ability_permission_em.name,
                code=ability_permission_em.code,
                ability_permission_id=ability_permission_em.id,
            )
            ability_permission_model = ability_permission_em.to_ability_permission_model()
            self.__ability_permission_repository.insert_ability_permission(
                data=ability_permission_model, transaction=transaction
            )
            child_resource_category = EnumChildResourceCategory.ABILITY_PERMISSION.name
        else:
            self.check_ability_permission_group(
                name=ability_permission_em.name,
                code=ability_permission_em.code,
                ability_permission_group_id=ability_permission_em.id,
            )
            ability_permission_group_model = (
                ability_permission_em.to_ability_permission_group_model()
            )
            self.__ability_permission_group_repository.insert_ability_permission_group(
                data=ability_permission_group_model, transaction=transaction
            )
            child_resource_category = EnumChildResourceCategory.ABILITY_PERMISSION_GROUP.name
        seq = self.__ability_permission_tree_repository.get_max_seq_by_ability_permission_group_id(
            ability_permission_group_id=ability_permission_em.parent_id
        )
        if seq and len(seq) > 0 and seq[0]["max_seq"]:
            seq = seq[0]["max_seq"] + 1
        else:
            seq = 1
        ability_permission_tree_model = AbilityPermissionTreeModel(
            ability_permission_group_id=ability_permission_em.parent_id,
            child_resource_category=child_resource_category,
            child_resource_id=ability_permission_em.id,
            seq=seq,
        )
        self.__ability_permission_tree_repository.insert_ability_permission_tree(
            data=ability_permission_tree_model, transaction=transaction
        )
        return ability_permission_em.id

    def check_ability_permission(
        self,
        name: str,
        code: Optional[str],
        ability_permission_id: Optional[str] = None,
    ):
        """
        检查功能权限
        :param name:
        :param code:
        :param ability_permission_id:
        :return:
        """

        same_name = self.__ability_permission_repository.get_same_name_ability_permission(
            name=name, permission_id=ability_permission_id
        )
        if same_name:
            raise BusinessError("已存在同名的功能权限")
        if code:
            same_code = self.__ability_permission_repository.get_same_code_ability_permission(
                code=code, permission_id=ability_permission_id
            )
            if same_code:
                raise BusinessError("已存在相同编码的功能权限")

    def check_ability_permission_group(
        self,
        name: str,
        code: Optional[str],
        ability_permission_group_id: Optional[str] = None,
    ):
        """
        检查功能权限文件夹
        :param name:
        :param code:
        :param ability_permission_group_id:
        :return:
        """

        same_name = (
            self.__ability_permission_group_repository.get_same_name_ability_permission_group(
                name=name, ability_permission_group_id=ability_permission_group_id
            )
        )
        if same_name:
            raise BusinessError("已存在同名的功能权限分组")
        if code:
            same_code = (
                self.__ability_permission_group_repository.get_same_code_ability_permission_group(
                    code=code, ability_permission_group_id=ability_permission_group_id
                )
            )
            if same_code:
                raise BusinessError("已存在相同编码的功能权限分组")

    def build_full_ability_permission_tree(self) -> List[TreeNodeModel]:
        """
        构建功能权限树
        :return:
        """
        tree_list = self.__ability_permission_repository.get_ability_permission_tree_list()
        tree = list_to_tree(
            original_list=tree_list,
            tree_node_type=AbilityPermissionTreeViewModel,
            seq_attr="tree_seq",
        )
        return tree

    def update_ability_permission(
        self,
        ability_permission_em: AbilityPermissionEditModel,
        transaction: Transaction,
    ):
        """
        更新功能权限
        :param ability_permission_em:
        :param transaction:
        :return:
        """

        if ability_permission_em.node_type == "ABILITY_PERMISSION":
            self.check_ability_permission(
                name=ability_permission_em.name,
                code=ability_permission_em.code,
                ability_permission_id=ability_permission_em.id,
            )
            self.__ability_permission_repository.update_ability_permission(
                permission=ability_permission_em,
                transaction=transaction,
                limited_col_list=["name", "code"],
            )
        else:
            self.check_ability_permission_group(
                name=ability_permission_em.name,
                code=ability_permission_em.code,
                ability_permission_group_id=ability_permission_em.id,
            )
            self.__ability_permission_group_repository.update_ability_permission_group(
                permission=ability_permission_em,
                transaction=transaction,
                limited_col_list=["name", "code"],
            )

    def delete_ability_permission(self, permission_id: str, transaction: Transaction):
        """
        删除功能权限
        :param permission_id:
        :param transaction:
        :return:
        """
        permission_list = self.__ability_permission_repository.get_ability_permission_with_children(
            permission_id=permission_id
        )
        for permission in permission_list:
            if permission.node_type == "ABILITY_PERMISSION":
                self.__ability_permission_repository.delete_ability_permission(
                    permission_id=permission.id, transaction=transaction
                )
            else:
                self.__ability_permission_group_repository.delete_ability_permission_group(
                    permission_group_id=permission.id, transaction=transaction
                )
            self.__ability_permission_tree_repository.delete_ability_permission_tree(
                ability_permission_tree_id=permission.tree_id, transaction=transaction
            )

    def save_ability_permission_assign(
        self,
        ability_permission_assign_em: AbilityPermissionAssignEm,
        transaction: Transaction,
    ):
        """
        保存授权数据
        :param ability_permission_assign_em:
        :param transaction:
        :return:
        """
        original_ability_permission_assign_em_list = (
            self.__ability_permission_assign_repository.get_ability_permission_assign_em_by_params(
                assign_resource_category=ability_permission_assign_em.assign_resource_category,
                assign_resource_id=ability_permission_assign_em.assign_resource_id,
            )
        )
        for assign_em in original_ability_permission_assign_em_list:
            self.__ability_permission_assign_repository.delete_ability_permission_assign_by_id(
                ability_permission_assign_id=assign_em.id,
                transaction=transaction,
            )
        if len(ability_permission_assign_em.ability_permission_id_list) > 0:
            for ability_permission_id in ability_permission_assign_em.ability_permission_id_list:
                data = ability_permission_assign_em.to_ability_permission_assign_model(
                    ability_permission_id=ability_permission_id
                )
                exist = self.__ability_permission_repository.get_ability_permission_by_id(
                    ability_permission_id=ability_permission_id
                )
                if exist:
                    self.__ability_permission_assign_repository.insert_ability_permission_assign(
                        data=data,
                        transaction=transaction,
                    )

    def get_ability_permission_assign_tree(
        self, ability_permission_assign_em: AbilityPermissionAssignEm
    ):
        """
        获取权限树的授权详情数据
        """

        tree_list = self.__ability_permission_assign_repository.get_ability_permission_assign_tree(
            assign_resource_category=ability_permission_assign_em.assign_resource_category,
            assign_resource_id=ability_permission_assign_em.assign_resource_id,
        )
        tree = list_to_tree(
            original_list=tree_list,
            tree_node_type=AbilityPermissionAssignTreeViewModel,
            seq_attr="tree_seq",
        )
        return tree

from typing import List, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.datetime_helper import local_now

from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.dept_category_model import EnumDeptCategoryCode
from infra_backbone.model.dept_model import DeptModel, EditDeptModel
from infra_backbone.model.dept_tree_model import DeptTreeModel
from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel
from infra_backbone.model.dimension_model import EnumDimensionCategory, EnumDimensionCode
from infra_backbone.model.edit.add_dept_dept_category_map_em import AddDeptDeptCategoryMapEditModel
from infra_backbone.model.edit.add_dept_em import AddDeptEditModel
from infra_backbone.model.params.dept_tree_query_params import DeptTreeQueryParams
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.service.dept_dept_category_map_service import DeptDeptCategoryMapService
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.establishment_service import EstablishmentService
from infra_backbone.service.organization_service import OrganizationService
from infra_backbone.service.storage_service import StorageService


class DeptService:
    def __init__(
        self,
        dept_repository: DeptRepository,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        establishment_service: EstablishmentService,
        dimension_repository: DimensionRepository,
        dept_dept_category_map_service: DeptDeptCategoryMapService,
        organization_service: OrganizationService,
        dimension_service: DimensionService,
        storage_service: StorageService,
    ):
        self.__dept_repository = dept_repository
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__establishment_service = establishment_service
        self.__dimension_repository = dimension_repository
        self.__dept_dept_category_map_service = dept_dept_category_map_service
        self.__organization_service = organization_service
        self.__dimension_service = dimension_service
        self.__storage_service = storage_service

    def add_dept(self, params: EditDeptModel, transaction: Transaction):
        """
        添加部门
        :param params:
        :param transaction:
        :return:
        """
        exist_dept = self.check_dept_params(params=params)
        if exist_dept:
            raise BusinessError("请勿重复添加")
        dept_id = self.__dept_repository.insert_dept(
            data=params.to_dept_model(),
            transaction=transaction,
        )
        max_seq = self.__dimension_dept_tree_repository.get_dimension_dept_tree_max_seq(
            parent_dept_id=params.parent_dept_id,
            dimension_id=params.dimension_id,
        )
        self.__dimension_dept_tree_repository.insert_dimension_dept_tree(
            data=params.to_dimension_dept_tree_model(dept_id=dept_id, seq=max_seq + 1),
            transaction=transaction,
        )

    def check_dept_params(self, params: EditDeptModel):
        if params.name:
            if len(params.name) > 255:
                raise BusinessError("名称限填255个字符")
        else:
            raise BusinessError("请填写名称")
        if params.comments:
            if len(params.comments) > 255:
                raise BusinessError("描述限填255个字符")
        exist_dept = self.__dept_repository.get_exist_dept(
            dept_id=params.id,
            name=params.name,
            parent_id=params.parent_dept_id,
            dimension_id=params.dimension_id,
            organization_id=params.organization_id,
        )
        return exist_dept

    def get_dept_info(self, dimension_dept_tree_id: str, organization_id: str):
        """
        获取部门信息
        :param dimension_dept_tree_id:
        :param organization_id:
        :return:
        """
        return self.__dept_repository.get_dept_info(
            dimension_dept_tree_id=dimension_dept_tree_id,
            organization_id=organization_id,
        )

    def add_dept_info(self, data: AddDeptEditModel, transaction: Transaction):
        """
        添加部门
        :param data:
        :param transaction:
        :return:
        """

        if not data.dimension_id and data.dimension_category:
            dimension = self.__dimension_repository.get_dimension_by_category_and_organization_id(
                category=data.dimension_category, organization_id=data.organization_id
            )
            data.dimension_id = dimension.id

        self.__dept_repository.insert_dept(
            data=data.cast_to(cast_type=DeptModel), transaction=transaction
        )
        dimension_dept_tree_id = self.__dimension_dept_tree_repository.insert_dimension_dept_tree(
            data=DimensionDeptTreeModel(
                dimension_id=data.dimension_id,
                dept_id=data.id,
                parent_dept_id=data.parent_dept_id,
                seq=data.seq,
                started_on=local_now(),
            ),
            transaction=transaction,
        )
        if data.category_code:
            self.__dept_dept_category_map_service.add_dept_dept_category_map(
                dept_dept_category_map_data=data.cast_to(
                    cast_type=AddDeptDeptCategoryMapEditModel, dept_id=data.id
                ),
                transaction=transaction,
            )
            if data.category_code == EnumDeptCategoryCode.CLASS.name:
                capacity_list = [
                    (
                        EnumCapacityCode.HEAD_TEACHER.name,
                        EnumCapacityCode.HEAD_TEACHER.value,
                    ),
                    (EnumCapacityCode.TEACHER.name, EnumCapacityCode.TEACHER.value),
                    (EnumCapacityCode.STUDENT.name, EnumCapacityCode.STUDENT.value),
                ]
                for capacity in capacity_list:
                    self.__establishment_service.fetch_establishment_info(
                        dimension_dept_tree_id=dimension_dept_tree_id,
                        capacity_code=capacity[0],
                        transaction=transaction,
                    )
        if not data.category_code:
            capacity_list = [
                (EnumCapacityCode.LEADER.name, EnumCapacityCode.LEADER.value),
                (EnumCapacityCode.MEMBER.name, EnumCapacityCode.MEMBER.value),
            ]
            for capacity in capacity_list:
                self.__establishment_service.fetch_establishment_info(
                    dimension_dept_tree_id=dimension_dept_tree_id,
                    capacity_code=capacity[0],
                    transaction=transaction,
                )

    def update_dept(
        self,
        dept_info: DeptModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        self.__dept_repository.update_dept(
            data=dept_info, transaction=transaction, limited_col_list=limited_col_list
        )

    def get_dept_tree(self, params: DeptTreeQueryParams):
        """
        获取部门树
        :return:
        """
        organization = self.__organization_service.get_system_unique_organization()
        if params.dimension_category:
            dimension = self.__dimension_service.get_dimension_by_category_code_and_organization_id(
                code=params.dimension_code,
                category=params.dimension_category,
                organization_id=organization.id,
            )
        else:
            dimension = self.__dimension_service.get_dimension_by_category_code_and_organization_id(
                code=EnumDimensionCode.K12.name,
                category=EnumDimensionCategory.EDU.name,
                organization_id=organization.id,
            )
        if not dimension:
            raise BusinessError("未找到部门所在维度")
        params.dimension_id = dimension.id
        dept_tree_list = self.__dept_repository.get_dept_tree_list(params=params)
        tree = list_to_tree(
            original_list=dept_tree_list,
            tree_node_type=DeptTreeModel,
        )
        # 用组织做假根
        tree_root = [
            DeptTreeModel(
                id=organization.id,
                key=organization.id,
                name=organization.name,
                level=0,
                parent_id=None,
                parent_name=None,
                dimension_dept_tree_id=None,
                comments=None,
                dept_category_code="ORGANIZATION",
                seq=0,
                child_list=tree,
            )
        ]
        return tree_root

    def get_dept_info_by_tree_id(self, tree_id: str) -> DeptModel:
        """
        根据获取部门信息
        :param tree_id:
        :return:
        """
        dept = self.__dept_repository.get_dept_by_tree_id(tree_id=tree_id)
        if not dept:
            raise BusinessError("未找到部门信息")
        return dept

    def get_dept_avatar_url(self, tree_id: str) -> str:
        """
        获取部门头像
        :param tree_id:
        :return:
        """
        dept = self.get_dept_info_by_tree_id(tree_id=tree_id)
        file_url = self.__storage_service.get_resource_file_url(
            resource=BasicResource(
                id=dept.id,
                category=EnumBackboneResource.DEPT.name,
            ),
            relationship=EnumFileRelationship.AVATAR.name,
        )
        if not file_url:
            raise BusinessError("未找到部门头像")
        return file_url

    def delete_dept(self, dept_id: str, transaction: Transaction):
        """
        删除部门
        :param dept_id:
        :param transaction:
        :return:
        """
        self.__dept_repository.delete_dept_by_id(dept_id=dept_id, transaction=transaction)

from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.datetime_helper import local_now

from infra_backbone.data.constant import DimensionCodeConst, OrganizationCodeConst
from infra_backbone.data.params.dept_tree_query_params import DeptTreeQueryParams
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.dept_category_model import EnumDeptCategoryCode
from infra_backbone.model.dept_model import AddDeptPeopleModel, DeptModel, EditDeptModel
from infra_backbone.model.dept_tree_model import DeptTreeModel
from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.edit.add_dept_dept_category_map_em import AddDeptDeptCategoryMapEditModel
from infra_backbone.model.edit.add_dept_em import AddDeptEditModel
from infra_backbone.model.establishment_model import EstablishmentModel
from infra_backbone.model.people_model import PeopleModel
from infra_backbone.model.position_model import EnumPosition
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.position_repository import PositionRepository
from infra_backbone.service.dept_dept_category_map_service import DeptDeptCategoryMapService
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.establishment_service import EstablishmentService
from infra_backbone.service.organization_service import OrganizationService
from infra_backbone.service.people_service import PeopleService


class DeptService:
    def __init__(
        self,
        dept_repository: DeptRepository,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        people_service: PeopleService,
        establishment_service: EstablishmentService,
        position_repository: PositionRepository,
        dimension_repository: DimensionRepository,
        dept_dept_category_map_service: DeptDeptCategoryMapService,
        organization_service: OrganizationService,
        dimension_service: DimensionService,
    ):
        self.__dept_repository = dept_repository
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__people_service = people_service
        self.__establishment_service = establishment_service
        self.__position_repository = position_repository
        self.__dimension_repository = dimension_repository
        self.__dept_dept_category_map_service = dept_dept_category_map_service
        self.__organization_service = organization_service
        self.__dimension_service = dimension_service

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

    def add_dept_people(self, params: AddDeptPeopleModel, transaction: Transaction):
        """
        添加部门人员
        :param params:
        :param transaction:
        :return:
        """
        if not params.people_id_list:
            if params.name:
                if len(params.name) > 255:
                    raise BusinessError("姓名限填255个字符")
            else:
                raise BusinessError("请填写姓名")
            people_id = self.__people_service.add_people(
                people=PeopleModel(
                    name=params.name,
                    gender=params.gender,
                    is_available=True,
                ),
                transaction=transaction,
            )
            params.people_id_list = [people_id]
        position = self.__position_repository.get_position_by_code(code=EnumPosition.MEMBER.name)
        for people_id in params.people_id_list:
            self.__establishment_service.add_establishment(
                establishment=EstablishmentModel(
                    dimension_dept_tree_id=params.dimension_dept_tree_id,
                    position_id=position.id,
                    people_id=people_id,
                ),
                transaction=transaction,
            )

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
                start_at=local_now(),
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
                    (EnumCapacityCode.HEAD_TEACHER.name, EnumCapacityCode.HEAD_TEACHER.value),
                    (EnumCapacityCode.TEACHER.name, EnumCapacityCode.TEACHER.value),
                    (EnumCapacityCode.STUDENT.name, EnumCapacityCode.STUDENT.value),
                ]
                for capacity in capacity_list:
                    self.__establishment_service.fetch_establishment_info(
                        dimension_dept_tree_id=dimension_dept_tree_id,
                        capacity_code=capacity[0],
                        capacity_name=capacity[1],
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
                    capacity_name=capacity[1],
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
        organization = self.__organization_service.get_organization_by_code(
            code=OrganizationCodeConst.BJSYXX
        )
        if params.dimension_category:
            dimension = self.__dimension_service.get_dimension_by_category_code_and_organization_id(
                code=params.dimension_code,
                category=params.dimension_category,
                organization_id=organization.id,
            )
        else:
            dimension = self.__dimension_service.get_dimension_by_category_code_and_organization_id(
                code=DimensionCodeConst.DINGTALK_EDU,
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
                children=tree,
            )
        ]
        return tree_root

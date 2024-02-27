from infra_basic.errors.input import DataNotFoundError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree

from infra_backbone.model.dept_model import DeptModel
from infra_backbone.model.dept_tree_model import DeptTreeNodeModel
from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel
from infra_backbone.model.edit.add_dimension_dept_em import AddDimensionDeptEditModel
from infra_backbone.model.params.dept_tree_query_params import DeptTreeQueryParams
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.repository.dimension_repository import DimensionRepository


class DimensionDeptTreeService:
    def __init__(
        self,
        dept_repository: DeptRepository,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        dimension_repository: DimensionRepository,
    ):
        self.__dept_repository = dept_repository
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__dimension_repository = dimension_repository

    def get_dimension_dept_tree(
        self,
        dimension_id: str,
        organization_id: str,
    ):
        """
        根据维度id和组织id获取部门树列表
        :param dimension_id:
        :param organization_id:
        :return:
        """
        tree_list = self.__dept_repository.get_dept_tree(
            dimension_id=dimension_id,
            organization_id=organization_id,
            search_text="",
        )
        tree = list_to_tree(
            original_list=tree_list,
            tree_node_type=DeptTreeNodeModel,
        )
        return tree

    def add_dimension_dept(self, data: AddDimensionDeptEditModel, transaction: Transaction):
        """
        添加部门
        :param data:
        :param transaction:
        :return:
        """

        dept_id = self.__dept_repository.insert_dept(
            data=data.cast_to(cast_type=DeptModel), transaction=transaction
        )
        self.__dimension_dept_tree_repository.insert_dimension_dept_tree(
            data=data.cast_to(cast_type=DimensionDeptTreeModel, dept_id=dept_id),
            transaction=transaction,
        )

    def get_dimension_dept_tree_by_code(self, params: DeptTreeQueryParams):
        """
        根据维度编码和组织id获取部门树列表
        :param params:
        :return:
        """
        dimension = self.__dimension_repository.get_dimension_by_category_code_and_organization_id(
            category=params.category,
            code=params.dimension_code,
            organization_id=params.organization_id,
        )
        if not dimension:
            raise DataNotFoundError("未获取到维度")
        tree_list = self.__dept_repository.get_dept_tree(
            dimension_id=dimension.id,
            organization_id=params.organization_id,
            search_text=params.search_text,
            is_available=params.is_available,
        )
        tree = list_to_tree(
            original_list=tree_list,
            tree_node_type=DeptTreeNodeModel,
        )
        return tree

    def get_dimension_dept_tree_by_dept_id_and_dimension(
        self, dimension_category: str, dept_id: str, organization_id: str
    ) -> DimensionDeptTreeModel:
        """

        :param dimension_category:
        :param dept_id:
        :param organization_id:
        :return:
        """

        dimension = self.__dimension_repository.get_dimension_by_category_and_organization_id(
            category=dimension_category, organization_id=organization_id
        )
        return self.__dimension_dept_tree_repository.get_dimension_dept_tree_by_dimension_id_and_dept_id(
            dimension_id=dimension.id, dept_id=dept_id
        )

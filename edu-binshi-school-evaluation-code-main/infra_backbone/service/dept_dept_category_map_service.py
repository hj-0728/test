from typing import Optional

from infra_basic.transaction import Transaction

from infra_backbone.model.dept_category_model import DeptCategoryModel
from infra_backbone.model.dept_dept_category_map_model import DeptDeptCategoryMapModel
from infra_backbone.model.edit.add_dept_dept_category_map_em import AddDeptDeptCategoryMapEditModel
from infra_backbone.repository.dept_category_repository import DeptCategoryRepository
from infra_backbone.repository.dept_dept_category_map_repository import (
    DeptDeptCategoryMapRepository,
)
from infra_backbone.service.dept_category_service import DeptCategoryService


class DeptDeptCategoryMapService:
    def __init__(
        self,
        dept_dept_category_map_repository: DeptDeptCategoryMapRepository,
        dept_category_service: DeptCategoryService,
    ):
        self.__dept_dept_category_map_repository = dept_dept_category_map_repository
        self.__dept_category_service = dept_category_service

    def add_dept_dept_category_map(
        self,
        dept_dept_category_map_data: AddDeptDeptCategoryMapEditModel,
        transaction: Optional[Transaction],
    ) -> str:
        """
        获取部门与部门类型关系
        :param dept_dept_category_map_data:
        :param transaction:
        :return:
        """
        dept_category_id = dept_dept_category_map_data.dept_category_id
        if not dept_category_id:
            dept_category = self.__dept_category_service.get_dept_category(
                code=dept_dept_category_map_data.category_code,
                name=dept_dept_category_map_data.category_name,
                organization_id=dept_dept_category_map_data.organization_id,
                transaction=transaction,
            )
            if dept_category:
                dept_category_id = dept_category.id

        if dept_category_id:
            return self.__dept_dept_category_map_repository.insert_dept_dept_category_map(
                data=DeptDeptCategoryMapModel(
                    dept_id=dept_dept_category_map_data.dept_id,
                    dept_category_id=dept_category_id,
                ),
                transaction=transaction,
            )

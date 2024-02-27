from typing import Optional

from infra_basic.transaction import Transaction

from infra_backbone.model.dept_category_model import DeptCategoryModel
from infra_backbone.repository.dept_category_repository import DeptCategoryRepository


class DeptCategoryService:
    def __init__(
        self,
        dept_category_repository: DeptCategoryRepository,
    ):
        self.__dept_category_repository = dept_category_repository

    def get_dept_category(
        self,
        code: str,
        name: Optional[str],
        organization_id: Optional[str],
        transaction: Optional[Transaction],
    ) -> Optional[DeptCategoryModel]:
        """
        获取部门类型
        :param code:
        :param name:
        :param organization_id:
        :param transaction:
        :return:
        """
        dept_category = self.__dept_category_repository.fetch_dept_category_by_code(code=code)
        if not dept_category and name and organization_id and transaction:
            dept_category = DeptCategoryModel(
                organization_id=organization_id,
                name=name,
                code=code,
            )
            dept_category.id = self.__dept_category_repository.insert_dept_category(
                data=dept_category, transaction=transaction
            )
        return dept_category

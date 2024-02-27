from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dept_category import DeptCategoryEntity
from infra_backbone.model.dept_category_model import DeptCategoryModel


class DeptCategoryRepository(BasicRepository):
    def insert_dept_category(self, data: DeptCategoryModel, transaction: Transaction) -> str:
        """
        插入部门类型
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DeptCategoryEntity, entity_model=data, transaction=transaction
        )

    def fetch_dept_category_by_code(self, code: str) -> Optional[DeptCategoryModel]:
        """
        获取部门类型根据code
        :param code:
        :return:
        """

        sql = """
        select * from st_dept_category where code=:code
        """

        return self._fetch_first_to_model(
            model_cls=DeptCategoryModel, sql=sql, params={"code": code}
        )

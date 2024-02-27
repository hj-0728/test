from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dept_dept_category_map import DeptDeptCategoryMapEntity
from infra_backbone.model.dept_dept_category_map_model import DeptDeptCategoryMapModel


class DeptDeptCategoryMapRepository(BasicRepository):
    def insert_dept_dept_category_map(
        self, data: DeptDeptCategoryMapModel, transaction: Transaction
    ) -> str:
        """
        插入部门类型
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DeptDeptCategoryMapEntity, entity_model=data, transaction=transaction
        )

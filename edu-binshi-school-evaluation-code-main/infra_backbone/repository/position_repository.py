from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.position import PositionEntity
from infra_backbone.model.position_model import PositionModel


class PositionRepository(BasicRepository):
    def insert_position(self, data: PositionModel, transaction: Transaction) -> str:
        """
        插入职位
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=PositionEntity, entity_model=data, transaction=transaction
        )

    def get_position_by_code(self, code: str) -> Optional[PositionModel]:
        """
        根据code获取职位
        :param code:
        :return:
        """

        sql = """select * from st_position where code = :code"""
        return self._fetch_first_to_model(model_cls=PositionModel, sql=sql, params={"code": code})

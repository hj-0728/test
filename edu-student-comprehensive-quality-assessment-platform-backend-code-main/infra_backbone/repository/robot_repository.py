from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.robot import RobotEntity
from infra_backbone.model.robot_model import RobotModel


class RobotRepository(BasicRepository):
    def insert_robot(self, data: RobotModel, transaction: Transaction) -> str:
        """
        插入机器人
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=RobotEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_robot_by_code(self, code: str) -> Optional[RobotModel]:
        """
        根据code获取机器人
        :param code:
        :return:
        """

        sql = """select * from st_robot where code = :code"""
        return self._fetch_first_to_model(model_cls=RobotModel, sql=sql, params={"code": code})

from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.observation_point_log import ObservationPointLogEntity
from biz_comprehensive.model.observation_point_log_model import ObservationPointLogModel


class ObservationPointLogRepository(BasicRepository):
    def delete_observation_points_log(self, log_id: str, transaction: Transaction):
        """
        删除观察点日志
        """
        self._delete_versioned_entity_by_id(
            entity_id=log_id, entity_cls=ObservationPointLogEntity, transaction=transaction
        )

    def insert_observation_points_log(
        self, data: ObservationPointLogModel, transaction: Transaction
    ) -> str:
        """
        插入观测点日志
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=ObservationPointLogEntity, entity_model=data, transaction=transaction
        )

    def fetch_observation_point_log_by_id(
        self, observation_point_log_id: str
    ) -> Optional[ObservationPointLogModel]:
        """
        获取观测点日志
        :param observation_point_log_id:
        :return:
        """

        sql = """
        select * from st_observation_point_log where id =:observation_point_log_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=ObservationPointLogModel,
            params={"observation_point_log_id": observation_point_log_id},
        )

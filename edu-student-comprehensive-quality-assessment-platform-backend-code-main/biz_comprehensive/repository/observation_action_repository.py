from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.observation_action import ObservationActionEntity
from biz_comprehensive.entity.observation_action_produce import ObservationActionProduceEntity
from biz_comprehensive.model.observation_action_model import ObservationActionModel
from biz_comprehensive.model.observation_action_produce_model import ObservationActionProduceModel
from biz_comprehensive.model.view.observation_action_with_produce_vm import (
    ObservationActionWithProduceViewModel,
)


class ObservationActionRepository(BasicRepository):
    def fetch_observation_action_with_produce(
        self, action_id: str
    ) -> Optional[ObservationActionWithProduceViewModel]:
        """
        获取观察行为及其产出
        """
        sql = """
        select sa.id, json_agg(sp.*) as produce_list
        from st_observation_action sa
        inner join st_observation_action_produce sp on sa.id = sp.observation_action_id
        where sa.id = :action_id
        group by sa.id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=ObservationActionWithProduceViewModel,
            params={"action_id": action_id},
        )

    def delete_observation_action_produce(self, produce_id: str, transaction: Transaction):
        """
        删除观察行为产出
        """
        self._delete_versioned_entity_by_id(
            entity_id=produce_id, entity_cls=ObservationActionProduceEntity, transaction=transaction
        )

    def delete_observation_action(self, action_id: str, transaction: Transaction):
        """
        删除观察行为
        """
        self._delete_versioned_entity_by_id(
            entity_id=action_id, entity_cls=ObservationActionEntity, transaction=transaction
        )

    def insert_observation_action(
        self, data: ObservationActionModel, transaction: Transaction
    ) -> str:
        """
        插入观察行为
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=ObservationActionEntity, entity_model=data, transaction=transaction
        )

    def insert_observation_action_produce(
        self, data: ObservationActionProduceModel, transaction: Transaction
    ) -> str:
        """
        插入观察行为产出
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=ObservationActionProduceEntity, entity_model=data, transaction=transaction
        )

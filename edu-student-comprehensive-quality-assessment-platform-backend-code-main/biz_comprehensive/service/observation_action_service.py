from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction

from biz_comprehensive.model.edit.observation_action_em import SaveEvaluationObsActionEditModel
from biz_comprehensive.model.edit.observation_point_log_em import SaveObservationPointLogEditModel
from biz_comprehensive.model.observation_action_model import ObservationActionModel
from biz_comprehensive.model.observation_action_produce_model import (
    EnumObservationActionProduceResCategory,
    ObservationActionProduceModel,
)
from biz_comprehensive.model.observation_point_log_model import EnumObserveeResCategory
from biz_comprehensive.repository.observation_action_repository import ObservationActionRepository
from biz_comprehensive.service.observation_point_log_service import ObservationPointLogService


class ObservationActionService:
    def __init__(
        self,
        observation_action_repository: ObservationActionRepository,
        observation_point_log_service: ObservationPointLogService,
    ):
        self.__observation_action_repository = observation_action_repository
        self.__observation_point_log_service = observation_point_log_service

    def delete_observation_action(
        self, action_id: str, transaction: Transaction
    ) -> List[ObservationActionProduceModel]:
        """
        删除观察行为
        """
        action = self.__observation_action_repository.fetch_observation_action_with_produce(
            action_id=action_id
        )
        if not action:
            return []
        self.__observation_action_repository.delete_observation_action(
            action_id=action_id, transaction=transaction
        )
        for produce in action.produce_list:
            self.__observation_action_repository.delete_observation_action_produce(
                produce_id=produce.id, transaction=transaction
            )
            self.delete_observation_action_produce_res(produce=produce, transaction=transaction)
        return action.produce_list

    def delete_observation_action_produce_res(
        self, produce: ObservationActionProduceModel, transaction: Transaction
    ):
        """
        删除观察行为产出资源
        :param produce:
        :param transaction:
        :return:
        """
        if (
            produce.produce_res_category
            == EnumObservationActionProduceResCategory.OBSERVATION_POINT_LOG.name
        ):
            self.__observation_point_log_service.delete_observation_point_log(
                log_id=produce.produce_res_id, transaction=transaction
            )

    def save_observation_action_and_produce(
        self,
        action_data: ObservationActionModel,
        produce_list: List[BasicResource],
        transaction: Transaction,
    ):
        """
        保存观察行为
        :param action_data:
        :param produce_list:
        :param transaction:
        :return:
        """

        action_id = self.__observation_action_repository.insert_observation_action(
            data=action_data, transaction=transaction
        )

        for produce in produce_list:
            self.__observation_action_repository.insert_observation_action_produce(
                data=ObservationActionProduceModel(
                    observation_action_id=action_id,
                    produce_res_category=produce.res_category,
                    produce_res_id=produce.res_id,
                ),
                transaction=transaction,
            )

    def save_evaluation_observation_action(
        self, action_info: SaveEvaluationObsActionEditModel, transaction: Transaction
    ) -> List[BasicResource]:
        """
        保存评价观察动作
        :param action_info:
        :param transaction:
        :return:
        """

        produce_list = []

        for observation_point_info in action_info.observation_point_info:
            for i in range(observation_point_info.amount):

                observee_res_list = []

                if action_info.observee_dept_tree_id_list:
                    for dept_tree_id in action_info.observee_dept_tree_id_list:
                        observee_res_list.append(
                            BasicResource(
                                id=dept_tree_id, category=EnumObserveeResCategory.DIMENSION_DEPT_TREE.name
                            )
                        )

                if action_info.observee_establishment_assign_id_list:
                    for assign_id in action_info.observee_establishment_assign_id_list:
                        observee_res_list.append(
                            BasicResource(
                                id=assign_id, category=EnumObserveeResCategory.ESTABLISHMENT_ASSIGN.name
                            )
                        )
                for observee_res in observee_res_list:

                    observation_point_log_res = self.__observation_point_log_service.save_observation_point_log(
                        observation_point_log=action_info.cast_to(
                            SaveObservationPointLogEditModel,
                            observation_point_id=observation_point_info.observation_point_id,
                            observee_res=observee_res,
                        ),
                        transaction=transaction,
                    )
                    self.save_observation_action_and_produce(
                        action_data=action_info.cast_to(ObservationActionModel),
                        produce_list=[observation_point_log_res],
                        transaction=transaction,
                    )

                    produce_list.append(observation_point_log_res)

        return produce_list

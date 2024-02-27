from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.model.calc_trigger_model import EnumCalcTriggerInputResCategory
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.edit.observation_point_log_em import SaveObservationPointLogEditModel
from biz_comprehensive.model.observation_point_log_model import (
    EnumObserveeResCategory,
    ObservationPointLogModel,
)
from biz_comprehensive.repository.observation_point_log_repository import (
    ObservationPointLogRepository,
)
from infra_backbone.data.enum import EnumFileRelationship


class ObservationPointLogService:
    def __init__(
        self,
        observation_point_log_repository: ObservationPointLogRepository,
        object_storage_service: ObjectStorageService,
    ):
        self.__observation_point_log_repository = observation_point_log_repository
        self.__object_storage_service = object_storage_service

    def delete_observation_point_log(self, log_id: str, transaction: Transaction):
        """
        删除观察点日志
        """
        self.__observation_point_log_repository.delete_observation_points_log(
            log_id=log_id, transaction=transaction
        )

    def save_observation_point_log(
        self, observation_point_log: SaveObservationPointLogEditModel, transaction: Transaction
    ) -> BasicResource:
        """
        保存观测点日志
        :param observation_point_log:
        :param transaction:
        :return:
        """
        observation_point_log_id = (
            self.__observation_point_log_repository.insert_observation_points_log(
                data=observation_point_log.cast_to(
                    ObservationPointLogModel,
                    observee_res_category=observation_point_log.observee_res.res_category,
                    observee_res_id=observation_point_log.observee_res.res_id,
                ),
                transaction=transaction,
            )
        )
        resource = BasicResource(
            id=observation_point_log_id,
            category=EnumComprehensiveResource.OBSERVATION_POINT_LOG.name,
        )

        if not observation_point_log.file_id_list:
            return resource

        for file_id in observation_point_log.file_id_list:
            self.__object_storage_service.link_file_and_resource(
                file_id=file_id,
                resource=resource,
                relationship=EnumFileRelationship.ANNEX.name,
                transaction=transaction,
            )

        return resource

    def get_calc_resource_data_by_log_id(
        self, observation_point_log_id: str
    ) -> CalcResourceEditModel:
        """
        获取计算资源数据根据日志id
        :param observation_point_log_id:
        :return:
        """

        observation_point_log = (
            self.__observation_point_log_repository.fetch_observation_point_log_by_id(
                observation_point_log_id=observation_point_log_id
            )
        )

        if not observation_point_log:
            raise BusinessError("观测点日志不存在")

        return CalcResourceEditModel(
            input_res_category=EnumCalcTriggerInputResCategory.OBSERVATION_POINT.name,
            input_res_id=observation_point_log.observation_point_id,
            clue_res_category=EnumComprehensiveResource.OBSERVATION_POINT_LOG.name,
            clue_res_id=observation_point_log_id,
            owner_res_category=observation_point_log.observee_res_category,
            owner_res_id=observation_point_log.observee_res_id,
        )

from typing import Optional

from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.service.observation_point_log_service import ObservationPointLogService
from infra_backbone.model.distributed_task_log_model import EnumDistributedTaskLogSourceResCategory


class CalcResourceService:
    def __init__(
        self,
        observation_point_log_service: ObservationPointLogService,
    ):
        self.__observation_point_log_service = observation_point_log_service

    def get_calc_resource_data_by_source_res(
        self, source_res_category: str, source_res_id: str
    ) -> Optional[CalcResourceEditModel]:
        """
        获取计算资源数据根据来源资源
        :param source_res_category:
        :param source_res_id:
        :return:
        """

        if (
            source_res_category
            == EnumDistributedTaskLogSourceResCategory.OBSERVATION_POINT_LOG.name
        ):
            return self.__observation_point_log_service.get_calc_resource_data_by_log_id(
                observation_point_log_id=source_res_id,
            )

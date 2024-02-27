from typing import List

from infra_basic.pagination_carrier import PaginationCarrier
from infra_object_storage.service.object_storage_service import ObjectStorageService

from biz_comprehensive.model.observation_point_model import EnumObservationPointCategory
from biz_comprehensive.model.param.class_report_query_params import (
    ClassReportPageFilterParams,
    ClassReportQueryParams,
    EnumQueryCategory,
)
from biz_comprehensive.model.view.class_points_count_vm import ClassPointsCountViewModel
from biz_comprehensive.model.view.observation_log_vm import ObservationLogViewModel
from biz_comprehensive.model.view.ranking_item_vm import RankingItemViewModel
from biz_comprehensive.repository.class_report_repository import ClassReportRepository
from infra_backbone.model.people_model import PeopleModel


class ClassReportService:
    def __init__(
        self,
        class_report_repository: ClassReportRepository,
        object_storage_service: ObjectStorageService,
    ):
        self.__class_report_repository = class_report_repository
        self.__object_storage_service = object_storage_service

    def get_class_observation_points_count(
        self, params: ClassReportQueryParams
    ) -> ClassPointsCountViewModel:
        """
        获取观察点数量统计
        """
        data_list = self.__class_report_repository.fetch_class_observation_points_count(
            params=params
        )
        result = ClassPointsCountViewModel()
        for data in data_list:
            if data.category == EnumObservationPointCategory.COMMEND.name:
                result.addition_points = data.points
            else:
                result.subtraction_points = data.points
        return result

    def get_class_ranking(self, params: ClassReportQueryParams) -> List[RankingItemViewModel]:
        """
        获取排行榜
        """
        if params.category == EnumQueryCategory.TOP3_RANKING.name:
            # 获取前3名
            top3 = self.__class_report_repository.fetch_class_top3_ranking(params=params)
            if len(top3) < 3:
                # 不足3名补齐
                missing = self.__class_report_repository.fetch_top3_ranking_missing_people(
                    existed_assign_ids=[item.establishment_assign_id for item in top3],
                    tree_id=params.tree_id,
                    missing_count=3 - len(top3),
                )
                top3.extend(missing)
            return top3
        return self.__class_report_repository.fetch_class_full_ranking(params=params)

    def get_observation_teacher(
        self, params: ClassReportQueryParams, current_people_id: str
    ) -> List[PeopleModel]:
        """
        获取观察教师
        """
        data_list = self.__class_report_repository.fetch_observation_teacher(params=params)
        result = []
        for data in data_list:
            if data.id == current_people_id:
                data.name = "我的"
                result.insert(0, data)
            else:
                result.append(data)
        return result

    def get_observation_log_page_list(
        self, params: ClassReportPageFilterParams, current_people_id: str
    ) -> PaginationCarrier[ObservationLogViewModel]:
        """
        获取观察记录分页列表
        :param params:
        :param current_people_id:
        :return:
        """
        result = self.__class_report_repository.fetch_observation_log_page_list(params=params)
        is_self = params.performer_res_id == current_people_id
        for data in result.data:
            data.is_self = is_self
        return result

from typing import List, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService

from biz_comprehensive.data.constant import SceneConst
from biz_comprehensive.data.enum import EnumComprehensiveResource, EnumDictMetaCode
from biz_comprehensive.model.calc_trigger_model import EnumCalcTriggerInputResCategory
from biz_comprehensive.model.edit.save_observation_point_em import SaveObservationPointEditModel
from biz_comprehensive.model.observation_point_model import (
    EnumObservationPointCategory,
    ObservationPointModel,
)
from biz_comprehensive.model.param.scence_observation_point_query_params import (
    SceneObservationPointQueryParams,
)
from biz_comprehensive.model.view.file_vm import FileViewModel
from biz_comprehensive.model.view.observation_point_vm import (
    ObservationPointListViewModel,
    ObservationPointViewModel,
    SceneObservationPointViewModel,
)
from biz_comprehensive.repository.observation_point_repository import ObservationPointRepository
from biz_comprehensive.service.calc_service import CalcService
from biz_comprehensive.service.calc_trigger_service import CalcTriggerService
from biz_comprehensive.service.scene_observation_point_assign_service import (
    SceneObservationPointAssignService,
)
from infra_backbone.data.enum import EnumFileRelationship
from infra_backbone.repository.dict_repository import DictRepository
from infra_backbone.repository.file_public_link_repository import FilePublicLinkRepository


class ObservationPointService:
    def __init__(
        self,
        observation_point_repository: ObservationPointRepository,
        object_storage_service: ObjectStorageService,
        calc_service: CalcService,
        calc_trigger_service: CalcTriggerService,
        dict_repository: DictRepository,
        scene_observation_point_assign_service: SceneObservationPointAssignService,
        file_public_link_repository: FilePublicLinkRepository
    ):
        self.__observation_point_repository = observation_point_repository
        self.__object_storage_service = object_storage_service
        self.__calc_service = calc_service
        self.__calc_trigger_service = calc_trigger_service
        self.__dict_repository = dict_repository
        self.__scene_observation_point_assign_service = scene_observation_point_assign_service
        self.__file_public_link_repository = file_public_link_repository

    def save_observation_point(
        self, observation_point: SaveObservationPointEditModel, transaction: Transaction
    ):
        """
        保存观测点
        :param observation_point:
        :param transaction:
        :return:
        """

        observation_point_info = self.__observation_point_repository.get_observation_point_by_name(
            name=observation_point.name
        )

        if (
            observation_point_info
            and observation_point.id
            and observation_point_info.id != observation_point.id
        ):
            raise BusinessError("观测点名称已存在")

        observation_point_db = None

        if observation_point.id:
            observation_point_list = self.__observation_point_repository.fetch_observation_point(
                observation_point_id=observation_point.id
            )
            if not observation_point_list:
                raise BusinessError("观测点不存在")
            observation_point_db = observation_point_list[0]
            observation_point_id = observation_point.id
            self.__observation_point_repository.update_observation_point(
                data=observation_point.cast_to(ObservationPointModel),
                transaction=transaction,
                limited_col_list=["name"],
            )
        else:
            observation_point_id = self.__observation_point_repository.insert_observation_point(
                data=observation_point.cast_to(ObservationPointModel), transaction=transaction
            )

        self.save_observation_point_icon(
            observation_point_id=observation_point_id,
            new_file_id=observation_point.file_id,
            old_file_id=observation_point_db.file_id if observation_point_db else None,
            transaction=transaction,
        )

        if (
            not observation_point_db
            or observation_point_db.point_score != observation_point.point_score
        ):
            if (
                observation_point.category == EnumObservationPointCategory.TO_BE_IMPROVED.name
                and observation_point.point_score > 0
            ):
                observation_point.point_score *= -1
            self.__calc_service.save_observation_point_calc_points(
                observation_point_id=observation_point_id,
                observation_point_category=observation_point.category,
                point_score=observation_point.point_score,
                transaction=transaction,
            )

        self.__scene_observation_point_assign_service.save_observation_point_scene(
            observation_point_id=observation_point_id,
            scene_id_list=observation_point.scene_id_list
            if observation_point.scene_id_list is not None
            else [],
            transaction=transaction,
        )

    def save_observation_point_icon(
        self,
        observation_point_id: str,
        new_file_id: str,
        old_file_id: Optional[str],
        transaction: Transaction,
    ):
        """
        保存观测点图标
        :param observation_point_id:
        :param new_file_id:
        :param old_file_id:
        :param transaction:
        :return:
        """
        resource = BasicResource(
            id=observation_point_id,
            category=EnumComprehensiveResource.OBSERVATION_POINT.name,
        )

        if old_file_id and old_file_id != new_file_id:
            self.__object_storage_service.unlink_file_and_resource(
                file_id=old_file_id,
                resource=resource,
                relationship=EnumFileRelationship.ICON.name,
                transaction=transaction,
            )

        if not old_file_id or old_file_id != new_file_id:
            self.__object_storage_service.link_file_and_resource(
                file_id=new_file_id,
                resource=resource,
                relationship=EnumFileRelationship.ICON.name,
                transaction=transaction,
            )

    def get_observation_point_list(self) -> ObservationPointListViewModel:
        """
        获取观测点列表
        :return:
        """
        observation_point_list = self.__observation_point_repository.fetch_observation_point()

        commend_obs_point_list = []
        to_be_improved_obs_point_list = []

        for observation_point in observation_point_list:
            if not observation_point.file_url:
                observation_point.file_url = self.__object_storage_service.get_file_url(
                    file_id=observation_point.file_id
                )
            if observation_point.category == EnumObservationPointCategory.COMMEND.name:
                commend_obs_point_list.append(observation_point)
            else:
                to_be_improved_obs_point_list.append(observation_point)

        return ObservationPointListViewModel(
            commend_obs_point_list=commend_obs_point_list,
            to_be_improved_obs_point_list=to_be_improved_obs_point_list,
        )

    def delete_observation_point(self, observation_point_id: str, transaction: Transaction):
        """
        删除观测点
        :param observation_point_id:
        :param transaction:
        :return:
        """

        self.__observation_point_repository.delete_observation_point(
            observation_point_id=observation_point_id, transaction=transaction
        )

        self.__calc_trigger_service.delete_calc_trigger_and_calc_by_input_res(
            input_res_category=EnumCalcTriggerInputResCategory.OBSERVATION_POINT.name,
            input_res_id=observation_point_id,
            transaction=transaction,
        )

    def get_observation_point_system_icon(self, category: str) -> List[FileViewModel]:
        """
        获取系统观测点图标
        :param category:
        :return:
        """

        if category == EnumObservationPointCategory.COMMEND.name:
            dict_meta_code = EnumDictMetaCode.SYSTEM_COMMEND_OBSERVATION_POINT_ICON.name
        else:
            dict_meta_code = EnumDictMetaCode.SYSTEM_TO_BE_IMPROVED_OBSERVATION_POINT_ICON.name

        icon_list = self.__dict_repository.get_dict_data_by_meta_code(dict_meta_code=dict_meta_code)

        file_ids = [x.value for x in icon_list]

        file_public_link_list = self.__file_public_link_repository.fetch_file_public_link_by_file_ids(file_ids=file_ids)

        file_public_link_file_ids = [x.file_id for x in file_public_link_list]

        need_get_url_ids = list(set(file_ids) - set(file_public_link_file_ids))

        file_list = []

        for file_public_link in file_public_link_list:
            file_list.append(
                FileViewModel(
                    id=file_public_link.file_id,
                    file_url=file_public_link.public_link,
                )
            )

        for file_id in need_get_url_ids:
            file_list.append(
                FileViewModel(
                    id=file_id,
                    file_url=self.__object_storage_service.get_file_url(file_id=file_id),
                )
            )

        return file_list

    def get_observation_point_info(self, observation_point_id: str) -> ObservationPointViewModel:
        """
        获取观测点列表
        :return:
        """
        observation_point_list = self.__observation_point_repository.fetch_observation_point(
            observation_point_id=observation_point_id
        )

        if not observation_point_list:
            raise BusinessError("观测点不存在")

        observation_point = observation_point_list[0]
        if not observation_point.file_url:
            observation_point.file_url = self.__object_storage_service.get_file_url(
                file_id=observation_point.file_id
            )

        observation_point_scene_list = self.__scene_observation_point_assign_service.get_scene_observation_point_assign_list_by_observation_point_id(
            observation_point_id=observation_point_id
        )

        observation_point.scene_id_list = [x.scene_id for x in observation_point_scene_list]

        return observation_point

    def get_observation_point_list_by_scene_id(
        self, params: SceneObservationPointQueryParams, people_id: str
    ) -> List[SceneObservationPointViewModel]:
        """
        获取场景下的观测点列表
        :param params:
        :param people_id:
        :return:
        """
        if params.scene_id == SceneConst.USED_SCENE:
            observation_point_list = self.__observation_point_repository.get_used_observation_point_by_category_and_people(
                observation_point_category=params.observation_point_category,
                people_id=people_id,
            )
        else:
            observation_point_list = (
                self.__observation_point_repository.get_observation_point_list_by_scene_id(
                    params=params
                )
            )
        for observation_point in observation_point_list:
            if not observation_point.file_url:
                observation_point.file_url = self.__object_storage_service.get_file_url(
                    file_id=observation_point.file_id
                )
        return observation_point_list

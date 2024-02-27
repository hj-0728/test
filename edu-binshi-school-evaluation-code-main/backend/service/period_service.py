import logging

from flask_jwt_extended import get_jwt_identity
from infra_basic.redis_manager import RedisManager
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.serialize_helper import ORJSONPickle

from backend.data.constant import RedisConst
from backend.model.view.period_vm import PeriodVm
from backend.service.redis_service import RedisService
from edu_binshi.model.period_category_model import EnumPeriodCategoryCode
from edu_binshi.model.view.period_vm import PeriodTreeNodeVm
from edu_binshi.repository.period_repository import PeriodRepository
from infra_backbone.data.constant import SymbolConst


class PeriodService:
    def __init__(
        self,
        period_repository: PeriodRepository,
        redis_manager: RedisManager,
        redis_service: RedisService,
    ):
        self.__period_repository = period_repository
        self.__redis_client = redis_manager.redis_client
        self.__redis_service = redis_service

    def get_period_tree(
        self,
        period_category_code: str = None,
    ):
        """
        获取周期分页
        :return:
        """
        tree_list = self.__period_repository.get_period_tree_list(
            period_category_code=period_category_code
        )
        return list_to_tree(tree_list, tree_node_type=PeriodTreeNodeVm, seq_attr="start_at")

    def get_current_period(self) -> PeriodVm:
        """
        获取当前周期
        :return:
        """

        redis_key = RedisConst.PERIOD + SymbolConst.COLON + get_jwt_identity()

        data_content = self.__redis_client.get(name=redis_key)
        if data_content:
            try:
                period_profile = ORJSONPickle.decode_model(
                    data_content=data_content,
                    data_type=PeriodVm,
                )
            except Exception as err:
                logging.error(err)
                period_profile = None
        else:
            period_profile = None

        if not period_profile:
            #  默认获取当前学期
            period = self.__period_repository.get_current_period_info_by_period_category(
                period_category=EnumPeriodCategoryCode.SEMESTER.name
            )

            period_profile = period.cast_to(PeriodVm)

            self.__redis_service.set_redis_period(
                period_profile=period_profile,
                redis_key=redis_key,
            )

        return period_profile

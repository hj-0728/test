from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.points_log import PointsLogEntity
from biz_comprehensive.model.causation_model import EnumCausationEffectResCategory
from biz_comprehensive.model.points_log_model import EnumPointsLogStatus, PointsLogModel


class PointsLogRepository(BasicRepository):
    def insert_points_log(self, data: PointsLogModel, transaction: Transaction) -> str:
        """
        插入积分日志
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=PointsLogEntity, entity_model=data, transaction=transaction
        )

    def update_points_log(
        self,
        data: PointsLogModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新积分日志
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=PointsLogEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_last_points_log_by_owner_res_and_symbol(
        self, owner_res_id: str, owner_res_category: str, symbol_id: str
    ) -> Optional[PointsLogModel]:
        """
        根据所属资源获取最后一条积分日志
        :param owner_res_id:
        :param owner_res_category:
        :param symbol_id:
        :return:
        """

        sql = """
        select * from st_points_log 
        where owner_res_id =:owner_res_id and owner_res_category =:owner_res_category
        and symbol_id=:symbol_id and status !=:status
        order by handled_on desc limit 1
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=PointsLogModel,
            params={
                "owner_res_id": owner_res_id,
                "owner_res_category": owner_res_category,
                "status": EnumPointsLogStatus.REVOKED.name,
                "symbol_id": symbol_id,
            },
        )

    def get_points_log_by_cause_res(
        self, cause_res_category: str, cause_res_id: str
    ) -> List[PointsLogModel]:
        """
        根据原因资源获取积分日志
        :param cause_res_category:
        :param cause_res_id:
        :return:
        """

        sql = """
        select p.* from st_causation c 
        inner join st_points_log p on c.effect_res_id = p.id and c.effect_res_category =:effect_res_category
        where c.cause_res_category =:cause_res_category and c.cause_res_id =:cause_res_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=PointsLogModel,
            params={
                "effect_res_category": EnumCausationEffectResCategory.POINTS_LOG.name,
                "cause_res_category": cause_res_category,
                "cause_res_id": cause_res_id,
            },
        )

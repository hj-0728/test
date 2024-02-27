from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.indicator_final_score import IndicatorFinalScoreEntity
from biz_comprehensive.model.indicator_final_score_model import IndicatorFinalScoreModel


class IndicatorFinalScoreRepository(BasicRepository):
    def insert_indicator_final_score(
        self, data: IndicatorFinalScoreModel, transaction: Transaction
    ) -> str:
        """
        插入指标最终得分
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=IndicatorFinalScoreEntity, entity_model=data, transaction=transaction
        )

    def get_indicator_final_score_by_owner_res_and_indicator(
        self, owner_res_id: str, owner_res_category: str, indicator_id: str
    ) -> Optional[IndicatorFinalScoreModel]:
        """
        根据所属资源获取指标最终得分
        :param owner_res_id:
        :param owner_res_category:
        :param indicator_id:
        :return:
        """

        sql = """
        select * from st_indicator_final_score 
        where owner_res_id =:owner_res_id 
        and owner_res_category =:owner_res_category
        and indicator_id=:indicator_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=IndicatorFinalScoreModel,
            params={
                "owner_res_id": owner_res_id,
                "owner_res_category": owner_res_category,
                "indicator_id": indicator_id,
            },
        )

    def update_indicator_final_score(
        self,
        data: IndicatorFinalScoreModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新指标最终得分
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        self._update_versioned_entity_by_model(
            entity_cls=IndicatorFinalScoreEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

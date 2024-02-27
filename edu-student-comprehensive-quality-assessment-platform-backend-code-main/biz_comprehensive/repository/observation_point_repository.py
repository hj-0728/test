from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.entity.observation_point import ObservationPointEntity
from biz_comprehensive.model.calc_rule_model import EnumBelongsToResCategory
from biz_comprehensive.model.observation_action_produce_model import (
    EnumObservationActionProduceResCategory,
)
from biz_comprehensive.model.observation_point_model import ObservationPointModel
from biz_comprehensive.model.param.scence_observation_point_query_params import (
    SceneObservationPointQueryParams,
)
from biz_comprehensive.model.scene_terminal_assign_model import EnumSceneTerminalCategory
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.observation_point_vm import (
    ObservationPointViewModel,
    SceneObservationPointViewModel,
)
from infra_backbone.data.enum import EnumFileRelationship


class ObservationPointRepository(BasicRepository):
    def insert_observation_point(
        self, data: ObservationPointModel, transaction: Transaction
    ) -> str:
        """
        插入菜单
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ObservationPointEntity, entity_model=data, transaction=transaction
        )

    def update_observation_point(
        self,
        data: ObservationPointModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        编辑观测点
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        self._update_versioned_entity_by_model(
            entity_cls=ObservationPointEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_observation_point(self, observation_point_id: str, transaction: Transaction):
        """
        删除观测点
        :param observation_point_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=ObservationPointEntity,
            entity_id=observation_point_id,
            transaction=transaction,
        )

    def fetch_observation_point(
        self, observation_point_id: str = None
    ) -> List[ObservationPointViewModel]:
        """
        获取观测点列表
        :param observation_point_id:
        :return:
        """
        sql = """
        select op.*, fr.file_id,cr.calc_func_params->>'score' as point_score,pl.public_link as file_url
        from st_observation_point op 
        inner join st_file_relationship fr on op.id = fr.res_id and res_category = :res_category 
        and relationship =:relationship
        inner join st_calc_trigger ct on op.id = ct.input_res_id and input_res_category =:res_category
        inner join st_calc_rule cr on cr.id = ct.calc_rule_id
        and cr.belongs_to_res_category =:belongs_to_res_category
        inner join st_symbol s on cr.belongs_to_res_id=s.id and s.code=:symbol_code 
        left join st_file_public_link pl on pl.file_id=fr.file_id
        """
        if observation_point_id:
            sql += " where op.id=:observation_point_id "
        sql += " order by op.handled_on desc "
        return self._fetch_all_to_model(
            model_cls=ObservationPointViewModel,
            sql=sql,
            params={
                "res_category": EnumComprehensiveResource.OBSERVATION_POINT.name,
                "relationship": EnumFileRelationship.ICON.name,
                "observation_point_id": observation_point_id,
                "belongs_to_res_category": EnumBelongsToResCategory.SYMBOL.name,
                "symbol_code": EnumSymbolCode.POINTS.name,
            },
        )

    def get_observation_point_by_name(self, name: str) -> Optional[ObservationPointModel]:
        """
        根据名称获取观测点
        :param name:
        :return:
        """

        sql = """
        select * from st_observation_point where name=:name
        """

        return self._fetch_first_to_model(
            model_cls=ObservationPointModel, sql=sql, params={"name": name}
        )

    def get_observation_point_list_by_scene_id(
        self, params: SceneObservationPointQueryParams
    ) -> List[SceneObservationPointViewModel]:
        """
        根据场景id获取观测点列表
        :param params:
        :return:
        """
        sql = """
        SELECT op.*, fr.file_id, cr.calc_func_params->>'score' as point_score,pl.public_link as file_url
        FROM st_scene_observation_point_assign pa 
        INNER JOIN st_observation_point op on pa.observation_point_id = op.id
        inner join st_calc_trigger ct on op.id = ct.input_res_id 
        and input_res_category = :res_category
        inner join st_calc_rule cr on cr.id = ct.calc_rule_id
        and cr.belongs_to_res_category = :belongs_to_res_category
        inner join st_symbol s on cr.belongs_to_res_id=s.id 
        INNER JOIN st_file_relationship fr on fr.res_id = op.id 
        and fr.res_category = :res_category
        left join st_file_public_link pl on pl.file_id=fr.file_id
        WHERE pa.scene_id = :scene_id
        and op.category = :category AND s.code=:symbol_code
        and fr.relationship = :relationship
        """
        return self._fetch_all_to_model(
            model_cls=SceneObservationPointViewModel,
            sql=sql,
            params={
                "res_category": EnumComprehensiveResource.OBSERVATION_POINT.name,
                "relationship": EnumFileRelationship.ICON.name,
                "scene_id": params.scene_id,
                "category": params.observation_point_category,
                "belongs_to_res_category": EnumBelongsToResCategory.SYMBOL.name,
                "symbol_code": EnumSymbolCode.POINTS.name,
            },
        )

    def get_used_observation_point_by_category_and_people(
        self, observation_point_category: str, people_id: str
    ) -> List[SceneObservationPointViewModel]:
        """
        获取常用场景中观测点
        :param observation_point_category:
        :param people_id:
        :return:
        """
        sql = """
        with used_observation_point as (
        SELECT op.*
        FROM st_observation_point op
        INNER JOIN st_scene_observation_point_assign pa on pa.observation_point_id = op.id
        INNER JOIN st_scene_terminal_assign sta on sta.scene_id = pa.scene_id
        INNER JOIN st_observation_point_log opl on op.id = opl.observation_point_id
        INNER JOIN st_observation_action_produce oap on opl.id = oap.produce_res_id 
        and oap.produce_res_category = :produce_res_category
        INNER JOIN st_observation_action oa on oap.observation_action_id = oa.id
        WHERE oa.performer_res_id = :people_id and opl.handled_on > (CURRENT_TIMESTAMP - INTERVAL '7 day')
        AND sta.terminal_category = :terminal_category
        GROUP BY op.id HAVING count(op.id) > 0
        ORDER BY count(op.id) DESC
        limit 10
        )
        select op.*,fr.file_id, cr.calc_func_params->>'score' as point_score,pl.public_link as file_url
        from used_observation_point op
        inner join st_calc_trigger ct on op.id = ct.input_res_id 
        and input_res_category = :res_category
        inner join st_calc_rule cr on cr.id = ct.calc_rule_id
        and cr.belongs_to_res_category = :belongs_to_res_category
        inner join st_symbol s on cr.belongs_to_res_id=s.id 
        INNER JOIN st_file_relationship fr on fr.res_id = op.id 
        and fr.res_category = :res_category
        left join st_file_public_link pl on pl.file_id=fr.file_id
        WHERE op.category = :category AND s.code=:symbol_code
        and fr.relationship = :relationship
        """

        return self._fetch_all_to_model(
            model_cls=SceneObservationPointViewModel,
            sql=sql,
            params={
                "res_category": EnumComprehensiveResource.OBSERVATION_POINT.name,
                "relationship": EnumFileRelationship.ICON.name,
                "category": observation_point_category,
                "belongs_to_res_category": EnumBelongsToResCategory.SYMBOL.name,
                "symbol_code": EnumSymbolCode.POINTS.name,
                "people_id": people_id,
                "terminal_category": EnumSceneTerminalCategory.TEACHER_MOBILE.name,
                "produce_res_category": EnumObservationActionProduceResCategory.OBSERVATION_POINT_LOG.name,
            },
        )

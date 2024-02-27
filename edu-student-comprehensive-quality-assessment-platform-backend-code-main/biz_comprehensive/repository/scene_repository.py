from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.scene import SceneEntity
from biz_comprehensive.model.edit.scene_em import SceneEditModel
from biz_comprehensive.model.observation_action_produce_model import (
    EnumObservationActionProduceResCategory,
)
from biz_comprehensive.model.observation_point_model import EnumObservationPointCategory
from biz_comprehensive.model.scene_model import SceneModel
from biz_comprehensive.model.scene_terminal_assign_model import EnumSceneTerminalCategory
from biz_comprehensive.model.view.scene_statistics_vm import SceneStatisticVm
from biz_comprehensive.model.view.scene_vm import SceneViewModel


class SceneRepository(BasicRepository):
    """
    场景
    """

    def insert_scene(self, data: SceneModel, transaction: Transaction) -> str:
        """
        新增场景
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=SceneEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_scene(self, data: SceneModel, transaction: Transaction):
        """
        修改场景
        """
        return self._update_versioned_entity_by_model(
            entity_cls=SceneEntity,
            update_model=data,
            transaction=transaction,
        )

    def delete_scene(self, scene_id: str, transaction: Transaction):
        """
        删除场景
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=SceneEntity, entity_id=scene_id, transaction=transaction
        )

    def get_scene_model_by_scene_id(self, scene_id: str) -> Optional[SceneEditModel]:
        """
        根据scene_id获取scene
        """
        sql = """
        WITH observation_point_statistic AS (
            SELECT ssopa.scene_id, sop.category, COUNT(ssopa.observation_point_id) AS num
            FROM st_scene_observation_point_assign ssopa
            JOIN st_observation_point sop ON ssopa.observation_point_id = sop.id
            GROUP BY sop.category, ssopa.scene_id
        ),
        terminal_statistic AS (
            SELECT scene_id, array_agg(terminal_category) AS terminal_category_list
            FROM st_scene_terminal_assign
            GROUP BY scene_id
        )
        SELECT 
            ss.*, 
            ts.terminal_category_list,
            json_agg(DISTINCT pa.observation_point_id) AS observation_point_id_list
        FROM 
            st_scene ss
        LEFT JOIN 
            terminal_statistic ts ON ss.id = ts.scene_id
        LEFT JOIN 
            observation_point_statistic ops ON ss.id = ops.scene_id
        LEFT JOIN st_scene_observation_point_assign pa ON ss.id = pa.scene_id
        WHERE ss.id = :scene_id
        GROUP BY 
            ss.id, ts.terminal_category_list, ops.scene_id
        """
        return self._fetch_first_to_model(
            sql=sql, model_cls=SceneEditModel, params={"scene_id": scene_id}
        )

    def get_scene_by_name(self, name: str, scene_id: Optional[str] = None) -> Optional[SceneModel]:
        """
        根据名称获取场景
        """
        sql = """
        select * from st_scene where name = :name
        """
        if scene_id:
            sql += " and id != :scene_id"
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=SceneModel,
            params={
                "name": name,
                "scene_id": scene_id,
            },
        )

    def get_scene_list(self) -> List[SceneViewModel]:
        """
        获取场景列表
        """
        sql = """
        WITH observation_point_statistic AS (
            SELECT ssopa.scene_id, sop.category, COUNT(ssopa.observation_point_id) AS num
            FROM st_scene_observation_point_assign ssopa
            JOIN st_observation_point sop ON ssopa.observation_point_id = sop.id
            GROUP BY sop.category, ssopa.scene_id
        ),
        terminal_statistic AS (
            SELECT scene_id, array_agg(terminal_category) AS terminal_category_list
            FROM st_scene_terminal_assign
            GROUP BY scene_id
        )
        SELECT 
            ss.*, 
            ts.terminal_category_list,
            CASE 
                WHEN ops.scene_id IS NOT NULL 
                THEN json_agg(json_build_object('category', ops.category, 'num', ops.num)) 
                ELSE '[]'::json
            END AS observation_point_statistics
        FROM 
            st_scene ss
        LEFT JOIN 
            terminal_statistic ts ON ss.id = ts.scene_id
        LEFT JOIN 
            observation_point_statistic ops ON ss.id = ops.scene_id
        GROUP BY 
            ss.id, ts.terminal_category_list, ops.scene_id
        ORDER BY ss.name
        """
        return self._fetch_all_to_model(sql=sql, model_cls=SceneViewModel)

    def get_scene_with_observation_point_count(self, terminal: str) -> List[SceneStatisticVm]:
        """
        获取场景列表带有观测点数量
        :param terminal:
        :return:
        """
        sql = """
        SELECT ss.id, ss.name,
        count(op.*) FILTER (WHERE op.category=:commend)  as commend_obs_point_count, 
        count(op.*) FILTER (WHERE op.category=:to_be_improved)  as to_be_improved_obs_point_count 
        FROM st_scene ss 
        INNER JOIN st_scene_terminal_assign sta on ss.id = sta.scene_id
        INNER JOIN st_scene_observation_point_assign pa on ss.id = pa.scene_id
        INNER JOIN st_observation_point op on pa.observation_point_id = op.id
        WHERE sta.terminal_category = :terminal_category
        GROUP BY ss.id HAVING count(op.*) > 0
        order by ss.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=SceneStatisticVm,
            params={
                "terminal_category": terminal,
                "commend": EnumObservationPointCategory.COMMEND.name,
                "to_be_improved": EnumObservationPointCategory.TO_BE_IMPROVED.name,
            },
        )

    def get_used_scene_with_observation_point_count(
        self, people_id: str, terminal: str
    ) -> Optional[SceneStatisticVm]:
        """
        获取常用场景中观测点统计
        :param people_id:
        :param terminal:
        :return:
        """
        sql = """
        with used_observation_point as (
        SELECT op.id,op.category
        FROM st_observation_point op
        INNER JOIN st_scene_observation_point_assign pa on pa.observation_point_id = op.id
        INNER JOIN st_scene_terminal_assign sta on sta.scene_id = pa.scene_id
        INNER JOIN st_observation_point_log opl on op.id = opl.observation_point_id
        INNER JOIN st_observation_action_produce oap on opl.id = oap.produce_res_id 
        and oap.produce_res_category = :produce_res_category
        INNER JOIN st_observation_action oa on oap.observation_action_id = oa.id
        WHERE oa.performer_res_id = :people_id and opl.handled_on > (CURRENT_TIMESTAMP - INTERVAL '7 day')
        AND sta.terminal_category = :terminal_category
        GROUP BY op.id,op.category HAVING count(op.id) > 0
        ORDER BY count(op.id) DESC
        limit 10
        )
        SELECT null as id, '我常用的' as name, 
        count(id) FILTER (WHERE category=:commend)  as commend_obs_point_count, 
        count(id) FILTER (WHERE category=:to_be_improved)  as to_be_improved_obs_point_count 
        FROM used_observation_point
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=SceneStatisticVm,
            params={
                "people_id": people_id,
                "terminal_category": terminal,
                "produce_res_category": EnumObservationActionProduceResCategory.OBSERVATION_POINT_LOG.name,
                "commend": EnumObservationPointCategory.COMMEND.name,
                "to_be_improved": EnumObservationPointCategory.TO_BE_IMPROVED.name,
            },
        )

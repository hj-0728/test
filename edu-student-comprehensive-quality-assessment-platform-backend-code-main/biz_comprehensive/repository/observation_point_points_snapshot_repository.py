from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.entity.observation_point_points_snapshot import (
    ObservationPointPointsSnapshotEntity,
)
from biz_comprehensive.model.observation_point_points_snapshot_model import (
    ObservationPointPointsSnapshotModel,
)
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship


class ObservationPointPointsSnapshotRepository(BasicRepository):
    def fetch_observation_point_points_snapshot_source(
        self, observation_point_log_id: str
    ) -> List[ObservationPointPointsSnapshotModel]:
        """
        获取观测点积分快照
        :param observation_point_log_id:
        :return:
        """
        sql = """
        with observation_info as (
        select soa.id as observation_action_id, sp1.name as observation_action_performer_name,
        soa.performed_started_on as observation_on, sol.id as observation_point_log_id, sol.observation_point_id,
        coalesce(sp2.name, st.display_name) as observee_name,
        sop.name as observation_point_name, sop.category as observation_point_category,
        sr.public_link as observation_point_icon,
        coalesce(se.dimension_dept_tree_id, st.dimension_dept_tree_id) as dimension_dept_tree_id				
        from st_observation_point_log sol
        inner join st_observation_point sop on sop.id = sol.observation_point_id
        inner join sv_file_relationship_public_link sr on sr.res_id = sop.id and sr.res_category = :observation_point
        and sr.relationship = :icon
        inner join st_observation_action_produce sap on sol.id = sap.produce_res_id
        and sap.produce_res_category = :observation_point_log
        inner join st_observation_action soa on sap.observation_action_id = soa.id
        inner join st_people sp1 on soa.performer_res_category = 'PEOPLE' and soa.performer_res_id = sp1.id
        left join st_establishment_assign sea1 on sea1.id = sol.observee_res_id
        and sol.observee_res_category = :establishment_assign
        left join st_people sp2 on sp2.id = sea1.people_id
        left join st_establishment se on se.id = sea1.establishment_id
        left join sv_k12_dept_tree st on st.dimension_dept_tree_id = sol.observee_res_id
        and sol.observee_res_category = :dimension_dept_tree
        where sol.id = :observation_point_log_id
        ),
        scene as (
        select oi.observation_point_id, array_agg(distinct ss.id) as scene_ids
        from observation_info oi
        inner join st_scene_observation_point_assign sa on sa.observation_point_id = oi.observation_point_id
        inner join st_scene ss on ss.id = sa.scene_id
        group by oi.observation_point_id
        ),
        point_scene as (
        select oi.*, scene_ids
        from observation_info oi
        left join scene s on oi.observation_point_id = s.observation_point_id
        ),
        points as (
        select sl.owner_res_category, sl.owner_res_id, coalesce(sp.name, st.display_name) as owner_name,
        coalesce(si1.public_link, si2.public_link) as owner_avatar,
        ss.code as symbol_code, ss.numeric_precision, sl.gained_points, sl.belongs_to_period_id, sl.id as points_log_id
        from observation_info oi
        inner join st_causation sc on sc.cause_res_category = :observation_point_log
        and sc.cause_res_id = oi.observation_point_log_id
        inner join st_points_log sl on sl.id = sc.effect_res_id and sc.effect_res_category = :points_log
        inner join st_symbol ss on ss.id = sl.symbol_id
        left join st_establishment_assign sea1 on sea1.id = sl.owner_res_id
        and sl.owner_res_category = :establishment_assign
        left join st_people sp on sp.id = sea1.people_id
        left join sv_file_relationship_public_link si1 on si1.res_category = :people
        and si1.res_id = sp.id and si1.relationship = :avatar
        left join st_establishment se on se.id = sea1.establishment_id
        left join sv_k12_dept_tree st on st.dimension_dept_tree_id = sl.owner_res_id
        and sl.owner_res_category = :dimension_dept_tree
        left join sv_file_relationship_public_link si2 on si2.res_category = :dept
        and si2.res_id = st.id and si2.relationship = :avatar
        )
        select * from point_scene oi
        inner join points p on true
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ObservationPointPointsSnapshotModel,
            params={
                "observation_point_log_id": observation_point_log_id,
                "observation_point": EnumComprehensiveResource.OBSERVATION_POINT.name,
                "observation_point_log": EnumComprehensiveResource.OBSERVATION_POINT_LOG.name,
                "points_log": EnumComprehensiveResource.POINTS_LOG.name,
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "dimension_dept_tree": EnumBackboneResource.DIMENSION_DEPT_TREE.name,
                "people": EnumBackboneResource.PEOPLE.name,
                "dept": EnumBackboneResource.DEPT.name,
                "icon": EnumFileRelationship.ICON.name,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def insert_observation_point_points_snapshot(
        self, data: ObservationPointPointsSnapshotModel, transaction: Transaction
    ):
        """
        添加观测点积分快照
        :param data:
        :param transaction:
        :return:
        """
        self._insert_versioned_entity_by_model(
            entity_model=data,
            entity_cls=ObservationPointPointsSnapshotEntity,
            transaction=transaction,
        )

    def fetch_observation_point_points_snapshot(
        self, observation_action_id: str
    ) -> List[ObservationPointPointsSnapshotModel]:
        """
        获取观测点积分快照
        :param observation_action_id:
        :return:
        """
        sql = """
        select * from st_observation_point_points_snapshot
        where observation_action_id = :observation_action_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ObservationPointPointsSnapshotModel,
            params={
                "observation_action_id": observation_action_id,
            },
        )

    def delete_observation_point_points_snapshot(self, snapshot_id: str, transaction: Transaction):
        """
        删除观测点积分快照
        """
        self._delete_versioned_entity_by_id(
            entity_id=snapshot_id,
            entity_cls=ObservationPointPointsSnapshotEntity,
            transaction=transaction,
        )

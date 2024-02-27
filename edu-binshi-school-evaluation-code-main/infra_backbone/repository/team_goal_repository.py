from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.team_goal import TeamGoalEntity
from infra_backbone.model.team_goal_model import TeamGoalModel
from infra_backbone.model.view.team_goal_tree_vm import TeamGoalTreeViwModel
from infra_backbone.model.view.team_goal_vm import TeamGoalViewModel


class TeamGoalRepository(BasicRepository):
    """
    小组目标repository
    """

    def get_team_goal_tree(
        self,
        dimension_id: str,
        team_id: str,
        team_category_id: str,
    ) -> List[TeamGoalTreeViwModel]:
        """
        获取小组目标树（部门树）
        """
        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sdt.id AS key,sd.name,
        sd2.name AS parent_name,
        sdt.parent_dept_id AS parent_id,
        ARRAY[sdt.seq] AS seq_list,1 AS level,ARRAY[sdt.id::character varying] AS path_list,
        sdt.seq, sc.code AS dept_category_code
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id  and sd.finish_at > now()
        left join st_dept sd2 on sd2.id = sdt.parent_dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        LEFT JOIN st_dept_dept_category_map sm ON sm.dept_id = sd.id
        LEFT JOIN st_dept_category sc ON sc.id = sm.dept_category_id
        WHERE sdt.parent_dept_id IS NULL AND sdn.id = :dimension_id
        UNION ALL
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sdt.id AS key, sd.name,
        sd2.name AS parent_name,
        sdt.parent_dept_id AS parent_id,
        array_append(t.seq_list, sdt.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sdt.dept_id) AS path_list, sdt.seq,
        sc.code AS dept_category_code
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id  and sd.finish_at > now()
        left join st_dept sd2 on sd2.id = sdt.parent_dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        JOIN dept_tree t ON t.id = sdt.parent_dept_id
        LEFT JOIN st_dept_dept_category_map sm ON sm.dept_id = sd.id
        LEFT JOIN st_dept_category sc ON sc.id = sm.dept_category_id
        ),
        have_selected_dimension_dept_tree as (
        select stg.goal_id, string_agg(st.name, '；') as team_name from st_team_goal stg
        join st_team st on st.id = stg.team_id
        join st_team_category stc on stc.id = st.team_category_id
        where stc.id = :team_category_id and stg.finish_at > now() and st.finish_at > now()
        """
        if team_id:
            sql += """
            and st.id <> :team_id
            """
        sql += """
        group by stg.goal_id)
        SELECT dt.*,hsd.team_name,
        case when hsd.team_name is not null then true else false end as disable_checkbox
        FROM dept_tree dt
        left join have_selected_dimension_dept_tree hsd on hsd.goal_id = dt.dimension_dept_tree_id
        order by dt.seq_list
        """
        return self._fetch_all_to_model(
            model_cls=TeamGoalTreeViwModel,
            sql=sql,
            params={
                "dimension_id": dimension_id,
                "team_category_id": team_category_id,
                "team_id": team_id,
            },
        )

    def insert_team_goal(
        self,
        team_goal: TeamGoalModel,
        transaction: Transaction,
    ) -> str:
        """
        插入小组目标
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TeamGoalEntity, entity_model=team_goal, transaction=transaction
        )

    def update_team_goal(
        self,
        team_goal: TeamGoalModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新小组目标
        """
        self._update_versioned_entity_by_model(
            entity_cls=TeamGoalEntity,
            update_model=team_goal,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_team_goal_list_by_team_id(
        self,
        team_id: str,
    ) -> List[TeamGoalViewModel]:
        """
        根据team_id获得team_goal的数据
        """
        sql = """
        select stg.*, case when sd2.name is null then sd.name else sd2.name || '/' || sd.name end as goal_name
        from st_team_goal stg
        join st_dimension_dept_tree sddt on sddt.id = stg.goal_id
        join st_dept sd on sd.id = sddt.dept_id
        left join st_dept sd2 on sd2.id = sddt.parent_dept_id
        where stg.team_id= :team_id and stg.finish_at > now()
        """

        return self._fetch_all_to_model(
            model_cls=TeamGoalViewModel,
            sql=sql,
            params={
                "team_id": team_id,
            },
        )

    def get_have_selected_team_goal(self, team_category_id: str, team_id: Optional[str]):
        """
        获取已选小组目标
        """
        sql = """
        select stg.*, st.name as team_name from st_team_goal stg
        join st_team st on st.id = stg.team_id
        join st_team_category stc on stc.id = st.team_category_id
        where stc.id = :team_category_id and stg.finish_at > now() and st.finish_at > now()
        """
        if team_id:
            sql += """
            and st.id <> :team_id
            """
        return self._fetch_all_to_model(
            model_cls=TeamGoalViewModel,
            sql=sql,
            params={
                "team_category_id": team_category_id,
                "team_id": team_id,
            },
        )

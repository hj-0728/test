from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from infra_backbone.entity.team import TeamEntity
from infra_backbone.model.params.team_query_params import TeamQueryParams
from infra_backbone.model.team_goal_model import EnumTeamGoalActivity
from infra_backbone.model.team_model import TeamModel
from infra_backbone.model.view.team_vm import TeamViewModel


class TeamRepository(BasicRepository):
    """
    小组 repository
    """

    def get_team_page(self, current_user_id: str, query_params: TeamQueryParams) -> PaginationCarrier[TeamViewModel]:
        """
        获取小组分页列表
        """
        sql = """
        with team as (
        select st.*,
        string_agg(case when sdd.name is null then sd.name else sdd.name || '/' || sd.name end, '；') as team_goal
        from st_team st
        left join st_team_goal sg on sg.team_id = st.id and sg.finish_at = 'infinity'
        and sg.activity = :evaluation
        left join st_dimension_dept_tree sddt on sddt.id = sg.goal_id
        left join st_dept sd on sd.id = sddt.dept_id
        left join st_dept sdd on sdd.id = sddt.parent_dept_id
        where team_category_id = :team_category_id
        and st.finish_at = 'infinity'
        group by st.id
        ),
        team_member as (
        select id, array_agg(count || '个' || name) as member_list from (
        select t.id, sc.name, count(distinct sp.id)
        from team t
        inner join st_team_member sm on sm.team_id = t.id and sm.finish_at = 'infinity'
        inner join st_people sp on sp.id = sm.people_id
        inner join st_capacity sc on sc.id = sm.capacity_id
        group by t.id, sc.name
        )aa
        group by id
        )
        select t.*,
        t.handler_id = :current_user_id as is_self_create,
        sp.name as create_people_name, coalesce(tm.member_list, array[]::varchar[]) as member_list from team t
        join st_people_user spu on spu.user_id = t.handler_id
        join st_people sp on sp.id = spu.people_id
        left join team_member tm on t.id = tm.id
        """
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[OrderCondition(column_name="start_at", order="desc")],
            filter_columns=["name", "create_people_name", "team_goal"],
            params={
                "team_category_id": query_params.team_category_id,
                "evaluation": EnumTeamGoalActivity.EVALUATION.name,
                "current_user_id": current_user_id,
            },
        )
        return self._paginate(
            result_type=TeamViewModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def insert_team(
        self,
        team: TeamModel,
        transaction: Transaction,
    ) -> str:
        """
        插入小组
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TeamEntity, entity_model=team, transaction=transaction
        )

    def update_team(
        self, team: TeamModel, transaction: Transaction, col_list: Optional[List[str]] = None
    ):
        """
        更新小组
        """
        self._update_versioned_entity_by_model(
            entity_cls=TeamEntity,
            update_model=team,
            transaction=transaction,
            limited_col_list=col_list,
        )

    def get_team_modal_by_team_id(
        self,
        team_id: str,
    ) -> Optional[TeamModel]:
        """
        获取小组modal
        :param team_id:
        :return:
        """

        sql = """
        SELECT * FROM st_team stc
        WHERE stc.id = :team_id
        """

        return self._fetch_first_to_model(
            model_cls=TeamModel,
            sql=sql,
            params={
                "team_id": team_id,
            },
        )

    def get_existed_team_by_name_except_current_id(
        self,
        name: str,
        team_category_id: str,
        team_id: Optional[str],
    ) -> Optional[TeamModel]:
        """
        通过name获取小组类型
        :param name:
        :param team_category_id:
        :param team_id:
        :return:
        """
        sql = """
              select * from st_team st
              where st.name=:name and st.finish_at > now() and team_category_id = :team_category_id
              """

        if team_id:
            sql += """
                    AND id!=:team_id
                    """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=TeamModel,
            params={"name": name, "team_category_id": team_category_id, "team_id": team_id},
        )

    def get_team_name_by_id(
        self,
        team_id: Optional[str],
    ) -> Optional[TeamModel]:
        """
        根据id获取小组对应的name
        """
        sql = """
        select st.* from st_team st where st.id=:team_id and st.finish_at > current_timestamp
        
        """
        return self._fetch_first_to_model(sql=sql, model_cls=TeamModel, params={"team_id": team_id})

    def get_team_vm_by_team_id(self, team_id: str):
        """
        根据team_id获取team_vm
        """
        sql = """
        with team_member as (
        select sm.team_id,  sp.name || '(' || sc.name || ')' as member_name
        from st_team_member sm
        left join st_people sp on sp.id = sm.people_id
        left join st_capacity sc on sc.id = sm.capacity_id
        where sm.finish_at = 'infinity' and sm.team_id = :team_id
        order by sc.name
        )
        select t.*, 
         array_remove(array_agg(member_name), null)
         as member_list
        from st_team t
        left join team_member tm on tm.team_id = t.id
        where t.id = :team_id
        group by t.id
        """
        return self._fetch_first_to_model(
            model_cls=TeamViewModel,
            sql=sql,
            params={
                "team_id": team_id,
            },
        )

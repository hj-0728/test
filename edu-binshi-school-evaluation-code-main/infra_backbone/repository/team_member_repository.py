from typing import List, Optional

from infra_basic.basic_repository import BasicRepository, OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from infra_backbone.entity.team_member import TeamMemberEntity
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.params.team_can_select_people_query_params import (
    TeamCanSelectPeopleQueryParams,
)
from infra_backbone.model.params.team_member_query_params import TeamMemberQueryParams
from infra_backbone.model.team_member_model import TeamMemberModel
from infra_backbone.model.view.team_can_select_people_vm import TeamCanSelectPeopleViewModel
from infra_backbone.model.view.team_member_vm import TeamMemberViewModel


class TeamMemberRepository(BasicRepository):
    """
    小组成员 repository
    """

    def insert_team_member(
        self,
        team_member: TeamMemberModel,
        transaction: Transaction,
    ):
        """
        插入小组成员
        """
        self._insert_versioned_entity_by_model(
            entity_cls=TeamMemberEntity, entity_model=team_member, transaction=transaction
        )

    def update_team_member(
        self,
        team_member: TeamMemberModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新小组成员
        """
        self._update_versioned_entity_by_model(
            entity_cls=TeamMemberEntity,
            update_model=team_member,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_team_member_by_team_member_id(self, team_member_id: str) -> TeamMemberModel:
        """
        获取小组成员
        """
        sql = """
        select * from st_team_member where id = :team_member_id
        """
        return self._fetch_first_to_model(
            model_cls=TeamMemberModel,
            sql=sql,
            params={"team_member_id": team_member_id},
        )

    def get_team_member_list_page(self, query_params: TeamMemberQueryParams):
        """
        获取小组成员列表页
        """
        sql = """
        select stm.*, sp.name as people_name, sc.name as capacity_name from st_team_member stm
        join st_people sp on stm.people_id = sp.id
        join st_capacity sc on stm.capacity_id = sc.id
        where team_id = :team_id and stm.start_at <=now() and stm.finish_at >now()
        """
        if query_params.search_text:
            sql += """
            and sp.name ~ :search_text
            """
        sql += """
        order by stm.seq asc
        """
        return self._fetch_all_to_model(
            model_cls=TeamMemberViewModel,
            sql=sql,
            params={
                "team_id": query_params.team_id,
                "search_text": query_params.search_text,
            },
        )

    def get_team_member_list_by_team_id(self, team_id: str):
        """
        获取小组成员列表
        """
        sql = """
        select * from st_team_member where team_id = :team_id
        and start_at <= now() and finish_at > now() order by seq asc
        """
        return self._fetch_all_to_model(
            model_cls=TeamMemberModel,
            sql=sql,
            params={"team_id": team_id},
        )

    def get_max_seq_by_team_id_and_capacity_code(self, team_id: str, capacity_code: str) -> int:
        """
        获取小组成员最大序号
        """
        sql = """
        select stm.* from st_team_member stm
        join st_capacity sc on stm.capacity_id = sc.id
        where stm.team_id = :team_id and sc.code = :capacity_code
        and stm.start_at <= now() and stm.finish_at > now() order by stm.seq desc limit 1
        """
        team = self._fetch_first_to_model(
            model_cls=TeamMemberModel,
            sql=sql,
            params={
                "team_id": team_id,
                "capacity_code": capacity_code,
            },
        )
        team_seq = {
            EnumCapacityCode.HEAD_TEACHER.name: 0,
            EnumCapacityCode.TEACHER.name: 1000,
            EnumCapacityCode.LEADER.name: 2000,
            EnumCapacityCode.MEMBER.name: 3000,
            EnumCapacityCode.STUDENT.name: 4000,
        }
        return team.seq if team else team_seq.get(capacity_code, 0)

    def get_can_select_people_list_page(self, query_params: TeamCanSelectPeopleQueryParams):
        """
        获取可选人员列表
        """
        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id as dimension_dept_tree_id,
        case when sd3.name is null then sd.name else sd3.name || '/' || sd.name end as name,
        sdt.parent_dept_id, sdt.dept_id
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sd2 ON sd2.id = sdt.dimension_id
        left join st_dept sd3 on sd3.id = sdt.parent_dept_id
        where sd2.category = :dimension_category
        """
        if query_params.dimension_dept_tree_id:
            sql += """
                    AND sdt.id = :dimension_dept_tree_id
                    """
        else:
            sql += """
                    AND sdt.parent_dept_id IS NULL
                    """
        sql += """
                UNION ALL
                SELECT dt.id as dimension_dept_tree_id,
                case when sd3.name is null then sd.name else sd3.name || '/' || sd.name end as name,
                dt.parent_dept_id, dt.dept_id
                FROM st_dimension_dept_tree dt
                INNER JOIN st_dept sd ON sd.id = dt.dept_id
                left join st_dept sd3 on sd3.id = dt.parent_dept_id
                JOIN dept_tree t ON t.dept_id = dt.parent_dept_id
                where dt.start_at <=now() and dt.finish_at >=now()
                ),
                result AS (
                select sp.id as people_id, sp.name as people_name, sc.id as capacity_id,
                sp.id ||'&&' || sc.id ||'&&' || sc.code as people_capacity_id,
                sc.name as capacity_name, string_agg(dt.name, '；') as dept_name
                from st_establishment_assign sea
                join st_people sp on sp.id = sea.people_id
                join st_establishment se on se.id = sea.establishment_id
                join st_capacity sc on sc.id = se.capacity_id
                join dept_tree dt on dt.dimension_dept_tree_id = se.dimension_dept_tree_id
                where sea.start_at <=now() and sea.finish_at >=now()
                group by sp.id, sp.name, sc.id, sc.name
                ),
                team_member AS (
                select stm.people_id, stm.capacity_id, stm.people_id ||'&&' || stm.capacity_id || '&&' || sc.code
                as people_capacity_id
                from st_team_member stm
                join st_capacity sc on sc.id = stm.capacity_id
                where stm.team_id = :team_id and stm.start_at <=now() and stm.finish_at >=now())
                select r.people_capacity_id as id, r.people_id, r.people_name, r.capacity_id, r.capacity_name, r.dept_name
                from result r where r.people_capacity_id not in (select people_capacity_id from team_member)
                """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["people_name"],
            order_columns=[
                OrderCondition(column_name="people_name", order="asc"),
            ],
            params={
                "dimension_category": query_params.dimension_category,
                "dimension_dept_tree_id": query_params.dimension_dept_tree_id,
                "team_id": query_params.team_id,
            },
        )
        return self._paginate(
            result_type=TeamCanSelectPeopleViewModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_team_member_by_team_and_people_id(
        self, team_id: str, people_id: str
    ) -> List[TeamMemberModel]:
        """
        获取输入分数的日志通过id
        :param team_id:
        :param people_id:
        :return:
        """
        sql = """
        select * from cv_team_member where team_id = :team_id and people_id = :people_id
        """
        return self._fetch_all_to_model(
            model_cls=TeamMemberModel,
            sql=sql,
            params={
                "team_id": team_id,
                "people_id": people_id,
            },
        )

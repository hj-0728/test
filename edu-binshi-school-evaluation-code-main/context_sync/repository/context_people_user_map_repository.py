"""
上下文人用户关联 repository
"""
from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from context_sync.entity.context_people_user_map import ContextPeopleUserMapEntity
from context_sync.model.context_people_user_map_model import (
    ContextPeopleUserMapModel,
    EnumContextPeopleUserMapResCategory,
)
from context_sync.model.view.context_people_user_detail_vm import (
    ContextPeopleStudentDetailViewModel,
    ContextPeopleUserDetailViewModel,
)
from infra_backbone.model.people_model import PeopleModel


class ContextPeopleUserMapRepository(BasicRepository):
    """
    上下文人用户关联 repository
    """

    def insert_context_people_user_map(
        self,
        context_org_corp_map: ContextPeopleUserMapModel,
        transaction: Transaction,
    ) -> str:
        """
        添加上下文人用户关联
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ContextPeopleUserMapEntity,
            entity_model=context_org_corp_map,
            transaction=transaction,
        )

    def delete_context_people_user_map(
        self,
        context_people_user_map_id: str,
        transaction: Transaction,
    ):
        """
        添加上下文人用户关联
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=ContextPeopleUserMapEntity,
            entity_id=context_people_user_map_id,
            transaction=transaction,
        )

    def fetch_context_people_detail_by_corp_id(
        self, dingtalk_corp_id: str
    ) -> List[ContextPeopleUserDetailViewModel]:
        """
        根据corp_id获取上下文人家长关联
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        select um.*, p.version as people_version,p.name,p.is_available 
        from st_context_people_user_map um 
        inner join st_dingtalk_user kp on kp.id=um.res_id
        INNER JOIN st_people p on p.id=um.people_id
        where um.res_category=:res_category and kp.dingtalk_corp_id=:dingtalk_corp_id
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleUserDetailViewModel,
            sql=sql,
            params={
                "res_category": EnumContextPeopleUserMapResCategory.DINGTALK_USER.name,
                "dingtalk_corp_id": dingtalk_corp_id,
            },
        )

    def fetch_context_people_parent_detail_by_corp_id(
        self, dingtalk_corp_id: str
    ) -> List[ContextPeopleUserDetailViewModel]:
        """
        根据corp_id获取上下文人家长关联
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        with parent as (
        select um.*,p.version as people_version,p.name,p.is_available 
        from st_context_people_user_map um 
        inner join st_dingtalk_k12_parent kp on kp.id=um.res_id
        INNER JOIN st_people p on p.id=um.people_id
        where um.res_category=:res_category and kp.dingtalk_corp_id=:dingtalk_corp_id
        )
        select p.*, um.res_id as dingtalk_user_id
        from parent p
        left join st_context_people_user_map um on um.people_id=p.people_id and um.res_category='DINGTALK_USER'
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleUserDetailViewModel,
            sql=sql,
            params={
                "res_category": EnumContextPeopleUserMapResCategory.DINGTALK_K12_PARENT.name,
                "dingtalk_corp_id": dingtalk_corp_id,
            },
        )

    def fetch_context_people_student_detail_by_corp_id(
        self, dingtalk_corp_id: str
    ) -> List[ContextPeopleStudentDetailViewModel]:
        """
        根据corp_id获取上下文人学生关联
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        select um.*,p.version as people_version,p.name,p.is_available ,
        array_agg(distinct dt.dept_id) as dept_id_list, 
        json_agg(json_build_object('parent_id',pr.object_people_id,
        'relationship', pr.relationship)) as family_relationship
        from st_context_people_user_map um 
        inner join st_dingtalk_k12_student ks on ks.id=um.res_id
        INNER JOIN st_people p on p.id=um.people_id
        left JOIN st_establishment_assign ta on ta.people_id=p.id and ta.start_at<=now() and ta.finish_at>=now()
        left JOIN st_establishment se on ta.establishment_id=se.id
        left JOIN st_capacity c on c.id=se.capacity_id and c.code='STUDENT'
        left JOIN st_dimension_dept_tree dt on dt.id=se.dimension_dept_tree_id
        left JOIN st_dimension d on d.id=dt.dimension_id and d.category='EDU'
        left join st_people_relationship pr on pr.subject_people_id=p.id
        where um.res_category=:res_category and ks.dingtalk_corp_id=:dingtalk_corp_id
        GROUP BY um.id,p.version,p.name,p.is_available 
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleStudentDetailViewModel,
            sql=sql,
            params={
                "res_category": EnumContextPeopleUserMapResCategory.DINGTALK_K12_STUDENT.name,
                "dingtalk_corp_id": dingtalk_corp_id,
            },
        )

    def get_no_avatar_student_people(self):
        """
        获取没有头像的学生
        """
        sql = """
        select distinct sp.* from st_people sp
        join st_context_people_user_map ss on ss.people_id = sp.id
        join st_dingtalk_k12_student ks on ks.id = ss.res_id and ss.res_category = 'DINGTALK_K12_STUDENT'
        left join st_file_relationship sr on sr.res_id = sp.id
        where sr.id is null
        """
        return self._fetch_all_to_model(model_cls=PeopleModel, sql=sql)

"""
上下文人用户关联 repository
"""
from typing import List, Optional

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
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.dimension_model import EnumDimensionCode
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

    def fetch_context_people_dingtalk_k12_parent(self) -> List[ContextPeopleUserDetailViewModel]:
        """
        根据corp_id获取上下文人家长关联
        :return:
        """

        sql = """
        select um.*, p.version as people_version,p.name,p.is_activated, sm.id as second_user_id
        from st_context_people_user_map um
        inner join st_people p on p.id=um.people_id
        left join st_context_people_user_map sm on sm.people_id = p.id
        and sm.res_category=:dingtalk_user
        where um.res_category=:dingtalk_k12_parent
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleUserDetailViewModel,
            sql=sql,
            params={
                "dingtalk_k12_parent": EnumContextPeopleUserMapResCategory.DINGTALK_K12_PARENT.name,
                "dingtalk_user": EnumContextPeopleUserMapResCategory.DINGTALK_USER.name,
            },
        )

    def fetch_context_people_dingtalk_user(self) -> List[ContextPeopleUserDetailViewModel]:
        """
        根据corp_id获取上下文人员关联
        :return:
        """

        sql = """
        select um.*, p.version as people_version,p.name,p.is_activated
        from st_context_people_user_map um
        inner join st_people p on p.id=um.people_id
        left join st_context_people_user_map sm on sm.people_id = p.id
        and sm.res_category = :dingtalk_k12_parent
        where um.res_category = :dingtalk_user
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleUserDetailViewModel,
            sql=sql,
            params={
                "dingtalk_user": EnumContextPeopleUserMapResCategory.DINGTALK_USER.name,
                "dingtalk_k12_parent": EnumContextPeopleUserMapResCategory.DINGTALK_K12_PARENT.name,
            },
        )

    def fetch_context_people_dingtalk_k12_student(
        self,
    ) -> List[ContextPeopleStudentDetailViewModel]:
        """
        根据corp_id获取上下文人学生关联
        :return:
        """

        sql = """
        select um.*,p.version as people_version,p.name,p.is_activated ,
        array_agg(distinct dt.dept_id) as dept_id_list, 
        json_agg(json_build_object('parent_id',pr.object_people_id,
        'relationship', pr.relationship)) as family_relationship
        from st_context_people_user_map um
        inner join st_people p on p.id=um.people_id
        left join st_establishment_assign ta on ta.people_id=p.id
        left join st_establishment se on ta.establishment_id=se.id
        left join st_capacity c on c.id=se.capacity_id and c.code=:student
        left join st_dimension_dept_tree dt on dt.id=se.dimension_dept_tree_id
        left join st_dimension d on d.id=dt.dimension_id and d.code=:k12
        left join st_people_relationship pr on pr.subject_people_id=p.id
        where um.res_category=:dingtalk_k12_student
        group by um.id,p.version,p.name,p.is_activated 
        """

        return self._fetch_all_to_model(
            model_cls=ContextPeopleStudentDetailViewModel,
            sql=sql,
            params={
                "dingtalk_k12_student": EnumContextPeopleUserMapResCategory.DINGTALK_K12_STUDENT.name,
                "student": EnumCapacityCode.STUDENT.name,
                "k12": EnumDimensionCode.K12.name,
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

    def fetch_context_people_by_user_resource(
        self, res_id: str, res_category: str
    ) -> Optional[ContextPeopleUserMapModel]:
        """
        根据用户资源获取上下文人用户关联
        :param res_id:
        :param res_category:
        :return:
        """
        sql = """
        select * from st_context_people_user_map 
        where res_id=:res_id and res_category=:res_category
        """
        return self._fetch_first_to_model(
            model_cls=ContextPeopleUserMapModel,
            sql=sql,
            params={"res_id": res_id, "res_category": res_category},
        )

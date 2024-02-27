"""
k12教师科目 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from edu_binshi.data.query_params.teacher_query_params import TeacherPageQueryParams
from edu_binshi.entity.k12_teacher_subject import K12TeacherSubjectEntity
from edu_binshi.model.k12_teacher_subject_model import K12TeacherSubjectModel
from edu_binshi.model.view.k12_teacher_subject_vm import K12TeacherSubjectVm
from edu_binshi.model.view.k12_teacher_vm import K12TeacherVm
from infra_backbone.model.dimension_model import EnumDimensionCategory


class K12TeacherSubjectRepository(BasicRepository):
    """
    k12教师科目 repository
    """

    def insert_k12_teacher_subject(
        self,
        k12_teacher_subject: K12TeacherSubjectModel,
        transaction: Transaction,
    ):
        """
        添加k12教师科目
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=K12TeacherSubjectEntity,
            entity_model=k12_teacher_subject,
            transaction=transaction,
        )

    def update_k12_teacher_subject(
        self,
        k12_teacher_subject: K12TeacherSubjectModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新k12教师科目
        """
        return self._update_versioned_entity_by_model(
            entity_cls=K12TeacherSubjectEntity,
            update_model=k12_teacher_subject,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_k12_teacher_subject(
        self,
        k12_teacher_subject_id: str,
        transaction: Transaction,
    ):
        """
        删除k12教师科目
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=K12TeacherSubjectEntity,
            entity_id=k12_teacher_subject_id,
            transaction=transaction,
        )

    def get_k12_teacher_list_page(
        self,
        params: TeacherPageQueryParams,
    ) -> PaginationCarrier[K12TeacherVm]:
        """
        获取老师 分页
        :param params:
        :return:
        """

        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id as dimension_dept_tree_id,
        case when sd3.name is null then sd.name else sd3.name || '/' || sd.name end as name,
        sdt.parent_dept_id, sdt.dept_id,
        ARRAY[sdt.seq] AS seq_list,
        ARRAY[sd.name::character varying] AS dept_name_list
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sd2 ON sd2.id = sdt.dimension_id
        left join st_dept sd3 on sd3.id = sdt.parent_dept_id
        where sd2.category = :category
        """
        if params.dimension_dept_tree_id:
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
        dt.parent_dept_id, dt.dept_id,
        array_append(t.seq_list, dt.seq) AS seq_list,
        array_append(t.dept_name_list, sd.name) AS dept_name_list
        FROM st_dimension_dept_tree dt
        INNER JOIN st_dept sd ON sd.id = dt.dept_id
        left join st_dept sd3 on sd3.id = dt.parent_dept_id
        JOIN dept_tree t ON t.dept_id = dt.parent_dept_id
        where dt.start_at <=now() and dt.finish_at >=now()
        ),
        people_capacity_info AS (
        select sp.id as people_id, sp.name as people_name, dt.name as dept_name,
        dt.dept_name_list as dept_name_list, dt.dimension_dept_tree_id, dt.seq_list,
        string_agg(sc.name, '；') as capacity_name
        from st_establishment_assign sea
        join st_people sp on sp.id = sea.people_id
        join st_establishment se on se.id = sea.establishment_id
        join st_capacity sc on sc.id = se.capacity_id
        join dept_tree dt on dt.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sea.start_at <=now() and sea.finish_at >=now() and sc.code <> 'STUDENT'
        group by sp.id, sp.name, dt.name, dt.dimension_dept_tree_id, dt.dept_name_list, dt.seq_list
        ),
        result as (
        select r.people_id,r.people_name, r.dimension_dept_tree_id, r.seq_list,
        r.dept_name,r.dept_name_list, r.capacity_name, 
        string_agg(ss.name, '；') as subject_name
        from people_capacity_info r
        left join cv_k12_teacher_subject kts
        on kts.people_id = r.people_id and kts.dimension_dept_tree_id = r.dimension_dept_tree_id
        left join st_subject ss on ss.id = kts.subject_id
        group by r.people_id,r.people_name, r.dimension_dept_tree_id,
        r.dept_name, r.capacity_name, r.dept_name_list, r.seq_list
        )
        select * from result
        where 1=1
        """
        if params.subject_name_list:
            if 'NONE' in params.subject_name_list:
                sql += """
                and (subject_name ~ any(array[:subject_name_list]) or subject_name is null)
                """
            else:
                sql += """
                and subject_name ~ any(array[:subject_name_list])
                """
        if params.capacity_name_list:
            sql += """
            and capacity_name ~ any(array[:capacity_name_list])
            """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["people_name"],
            order_columns=[
                OrderCondition(column_name="seq_list", order="asc"),
                OrderCondition(column_name="people_name", order="asc"),
            ],
            params={
                "dimension_dept_tree_id": params.dimension_dept_tree_id,
                "category": EnumDimensionCategory.EDU.name,
                "capacity_name_list": params.capacity_name_list,
                "subject_name_list": params.subject_name_list,
            },
        )
        return self._paginate(
            result_type=K12TeacherVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_k12_teacher_subject_vm_list(
        self,
        people_id: str,
        dimension_dept_tree_id: str,
    ) -> List[K12TeacherSubjectVm]:
        """
        获取k12教师科目列表
        """
        sql = """
        select kts.*, ss.name as subject_name
        from cv_k12_teacher_subject kts
        join st_subject ss on ss.id = kts.subject_id
        where kts.people_id = :people_id and kts.dimension_dept_tree_id = :dimension_dept_tree_id
        """
        return self._fetch_all_to_model(
            model_cls=K12TeacherSubjectVm,
            sql=sql,
            params={
                "people_id": people_id,
                "dimension_dept_tree_id": dimension_dept_tree_id,
            },
        )

    def fetch_class_subject_other_teacher(
        self, dimension_dept_tree_id: str, subject_id: str, people_id: str
    ) -> Optional[K12TeacherSubjectVm]:
        """
        获取指定班级该科目除了当前老师，是否还有其他老师任教
        同一时间段内一个班级一个科目应该只有一个老师任教
        """
        sql = """
        select ss.*, sp.name as people_name
        from cv_k12_teacher_subject ss
        inner join st_people sp on sp.id = ss.people_id
        where dimension_dept_tree_id = :dimension_dept_tree_id
        and subject_id = :subject_id
        and people_id != :people_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=K12TeacherSubjectVm,
            params={
                "dimension_dept_tree_id": dimension_dept_tree_id,
                "subject_id": subject_id,
                "people_id": people_id,
            },
        )

    def fetch_k12_teacher_subject_by_id(
        self, k12_teacher_subject_id: str
    ) -> Optional[K12TeacherSubjectModel]:
        """
        获取k12教师科目
        """
        sql = """select * from st_k12_teacher_subject where id = :k12_teacher_subject_id"""
        return self._fetch_first_to_model(
            model_cls=K12TeacherSubjectModel,
            sql=sql,
            params={"k12_teacher_subject_id": k12_teacher_subject_id},
        )

    def get_need_delete_k12_teacher_subject(self) -> List[K12TeacherSubjectModel]:
        """
        获取需要删除的数据，判断老师是否还在班级
        :return:
        """

        sql = """
        with people_dept as (
        select ea.people_id,e.dimension_dept_tree_id 
        from cv_establishment_assign ea 
        INNER JOIN cv_establishment e on ea.establishment_id=e.id
        INNER JOIN st_capacity c on c.id=e.capacity_id
        where c.code=any(array['TEACHER', 'HEAD_TEACHER'])
        )
        select ts.* from st_k12_teacher_subject ts 
        left join people_dept pd on ts.people_id=pd.people_id 
        and ts.dimension_dept_tree_id=pd.dimension_dept_tree_id
        where ts.finish_at>now() and pd.people_id is null
        """

        return self._fetch_all_to_model(
            model_cls=K12TeacherSubjectModel,
            sql=sql,
        )

"""
科目 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.subject import SubjectEntity
from edu_binshi.model.subject_model import SubjectModel


class SubjectRepository(BasicRepository):
    """
    科目 repository
    """

    def insert_subject(
        self,
        subject: SubjectModel,
        transaction: Transaction,
    ):
        """
        添加科目
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=SubjectEntity, entity_model=subject, transaction=transaction
        )

    def update_subject(
        self,
        subject: SubjectModel,
        transaction: Transaction,
    ):
        """
        添加科目
        """
        return self._update_versioned_entity_by_model(
            entity_cls=SubjectEntity, update_model=subject, transaction=transaction
        )

    def get_subject_by_name(self, name: str) -> Optional[SubjectModel]:
        """
        获取科目
        """
        sql = """
        select * from st_subject where name = :name
        """
        return self._fetch_first_to_model(
            model_cls=SubjectModel,
            sql=sql,
            params={"name": name},
        )

    def get_subject_list(self) -> List[SubjectModel]:
        """
        获取科目列表
        """
        sql = """
        select * from st_subject where is_activated is True
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=SubjectModel,
        )

    def fetch_subject_list(self) -> List[SubjectModel]:
        """
        获取科目列表
        """
        sql = """
        select * from st_subject where is_activated is True
        """
        return self._fetch_all_to_model(SubjectModel, sql=sql)

    def fetch_subject_by_id(self, subject_id: str) -> Optional[SubjectModel]:
        """
        获取科目
        """
        sql = """
        select * from st_subject where id = :subject_id
        """
        return self._fetch_first_to_model(
            model_cls=SubjectModel,
            sql=sql,
            params={"subject_id": subject_id},
        )

"""
上下文组织关联 repository
"""
from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from context_sync.entity.context_organization_corp_map import ContextOrganizationCorpMapEntity
from context_sync.model.context_organization_corp_map_model import ContextOrganizationCorpMapModel


class ContextOrganizationCorpMapRepository(BasicRepository):
    """
    上下文组织关联 repository
    """

    def insert_context_organization_corp_map(
        self,
        context_org_corp_map: ContextOrganizationCorpMapModel,
        transaction: Transaction,
    ) -> str:
        """
        添加上下文组织关联
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ContextOrganizationCorpMapEntity,
            entity_model=context_org_corp_map,
            transaction=transaction,
        )

    def fetch_context_org_corp_map_by_res(
        self, res_category: str, res_id: str
    ) -> Optional[ContextOrganizationCorpMapModel]:
        """
        根据res获取上下文组织关联
        :param res_category:
        :param res_id:
        :return:
        """

        sql = """
        select * from st_context_organization_corp_map 
        where res_category=:res_category and res_id=:res_id
        """

        return self._fetch_first_to_model(
            model_cls=ContextOrganizationCorpMapModel,
            sql=sql,
            params={
                "res_category": res_category,
                "res_id": res_id,
            },
        )

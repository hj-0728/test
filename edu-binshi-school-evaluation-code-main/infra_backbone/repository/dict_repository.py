from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dict_data import DictDataEntity
from infra_backbone.entity.dict_meta import DictMetaEntity
from infra_backbone.model.dict_data_model import DictDataModel
from infra_backbone.model.dict_meta_model import DictMetaModel


class DictRepository(BasicRepository):
    def get_dict_by_meta_code_and_dict_data_code(
        self,
        dict_meta_code: str,
        dict_data_code: str,
    ) -> DictDataModel:
        """
        根据字典元和字典项的编码获取字典
        :param dict_meta_code:
        :param dict_data_code:
        :return:
        """

        sql = """select sdd.* from st_dict_meta sdm
        inner join st_dict_data sdd on sdd.dict_meta_id = sdm.id
        where sdm.code = :dict_meta_code
        and sdd.code = :dict_data_code"""
        return self._fetch_first_to_model(
            model_cls=DictDataModel,
            sql=sql,
            params={"dict_meta_code": dict_meta_code, "dict_data_code": dict_data_code},
        )

    def insert_dict_meta(self, dict_meta: DictMetaModel, transaction: Transaction) -> str:
        """
        插入字典元
        :param dict_meta:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DictMetaEntity, entity_model=dict_meta, transaction=transaction
        )

    def insert_dict_data(self, dict_data: DictDataModel, transaction: Transaction) -> str:
        """
        插入字典项
        :param dict_data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DictDataEntity, entity_model=dict_data, transaction=transaction
        )

    def get_dict_meta_by_code(self, code: str) -> Optional[DictMetaModel]:
        """
        根据code获取字典元
        :param code:
        :return:
        """

        sql = """
        SELECT * FROM st_meata WHERE code = :code
        """

        return self._fetch_first_to_model(model_cls=DictMetaModel, sql=sql, params={"code": code})

    def get_dict_data_by_meta_code(self, dict_meta_code: str) -> List[DictDataModel]:
        """
        根据字典元编码获取字典数据
        :param dict_meta_code:
        """
        sql = """
        select sdd.* from st_dict_data sdd
        INNER JOIN st_dict_meta sdm on sdm.id = sdd.dict_meta_id 
        WHERE sdm.code = :dict_meta_code
        """
        return self._fetch_all_to_model(
            model_cls=DictDataModel,
            sql=sql,
            params={"dict_meta_code": dict_meta_code},
        )

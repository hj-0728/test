from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.area import AreaEntity
from infra_backbone.model.area_model import AreaModel


class AreaRepository(BasicRepository):
    def insert_area(self, data: AreaModel, transaction: Transaction) -> str:
        """
        插入地域
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=AreaEntity, entity_model=data, transaction=transaction
        )

    def fetch_area_list(self, parent_id: Optional[str] = None) -> List[AreaModel]:
        """
        获取区域列表
        :param parent_id: 为空时获取省、直辖市一级
        :return:
        """
        sql = """select * from mv_area"""
        if parent_id:
            sql += """ where parent_id = :parent_id"""
        else:
            sql += """ where parent_id is null"""
        return self._fetch_all_to_model(
            model_cls=AreaModel, sql=sql, params={"parent_id": parent_id}
        )

    def fetch_area_with_parent_list(self, area_id: str) -> List[AreaModel]:
        """
        获取地域及父级地域列表
        :param area_id:
        :return:
        """
        sql = """select ma.* from mv_area ma
        inner join mv_area ma2 on ma.id = any(ma2.path_id_list)
        where ma2.id = :area_id
        """
        return self._fetch_all_to_model(model_cls=AreaModel, sql=sql, params={"area_id": area_id})

    def get_area_by_code(self, code) -> Optional[AreaModel]:
        """
        根据编码获得地域信息
        :param code:
        :return:
        """
        sql = """
        select * from st_area where zoning_code = :code
        """
        return self._fetch_first_to_model(model_cls=AreaModel, sql=sql, params={"code": code})

from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.search_hisotry import SearchHistoryEntity
from biz_comprehensive.model.search_history_model import SearchHistoryModel


class SearchHistoryRepository(BasicRepository):
    def insert_search_history(self, data: SearchHistoryModel, transaction: Transaction):
        """
        插入搜索历史
        """
        self._insert_versioned_entity_by_model(
            entity_cls=SearchHistoryEntity,
            entity_model=data,
            transaction=transaction,
        )

    def fetch_search_history(self, data: SearchHistoryModel) -> Optional[SearchHistoryModel]:
        """
        获取搜索历史
        :param data:
        :return:
        """
        sql = """select * from st_search_history
        where owner_people_id = :owner_people_id and search_content = :search_content and search_scene = :search_scene
        """
        return self._fetch_first_to_model(
            sql=sql,
            params=data.dict(),
            model_cls=SearchHistoryModel,
        )

    def update_search_history(self, data: SearchHistoryModel, transaction: Transaction):
        """
        更新搜索历史
        对搜索历史只可能更新search_on，其他字段若有变化，应该是新增一条数据，
        所以此处limited_col_list，我在repository方法中写死，不从service传
        """
        self._update_versioned_entity_by_model(
            entity_cls=SearchHistoryEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=["search_on"],
        )

    def fetch_people_search_history_list(
        self, people_id: str, search_scene: str, limit_count: Optional[int] = None
    ) -> List[SearchHistoryModel]:
        """
        获取人员搜索历史
        """
        sql = """
        select *
        from st_search_history
        where owner_people_id = :people_id and search_scene = :search_scene
        order by search_on desc
        """
        if limit_count:
            sql += f" limit {limit_count}"
        return self._fetch_all_to_model(
            sql=sql,
            params={"people_id": people_id, "search_scene": search_scene},
            model_cls=SearchHistoryModel,
        )

    def delete_search_history(self, search_history_id: str, transaction: Transaction):
        """
        删除搜索历史
        """
        self._delete_versioned_entity_by_id(
            entity_cls=SearchHistoryEntity,
            entity_id=search_history_id,
            transaction=transaction,
        )

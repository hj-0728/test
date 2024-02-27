from typing import List

from infra_basic.transaction import Transaction

from biz_comprehensive.model.search_history_model import SearchHistoryModel
from biz_comprehensive.repository.search_history_repository import SearchHistoryRepository


class SearchHistoryService:
    def __init__(self, search_history_repository: SearchHistoryRepository):
        self.__search_history_repository = search_history_repository

    def add_search_history(self, data: SearchHistoryModel, transaction: Transaction):
        """
        添加搜索历史
        :param data:
        :param transaction:
        :return:
        """
        search_history = self.__search_history_repository.fetch_search_history(data=data)
        if search_history:
            search_history.search_on = data.search_on
            self.__search_history_repository.update_search_history(
                data=search_history,
                transaction=transaction,
            )
        else:
            self.__search_history_repository.insert_search_history(
                data=data, transaction=transaction
            )

    def clear_search_history(self, search_scene: str, people_id: str, transaction: Transaction):
        """
        清空搜索历史
        :return:
        """
        search_history_list = self.__search_history_repository.fetch_people_search_history_list(
            people_id=people_id, search_scene=search_scene
        )
        for search_history in search_history_list:
            self.__search_history_repository.delete_search_history(
                search_history_id=search_history.id,
                transaction=transaction,
            )

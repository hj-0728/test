from typing import List, Optional

from infra_basic.transaction import Transaction

from infra_backbone.model.edit.dict_em import DictDataEm, DictMetaEm
from infra_backbone.repository.dict_repository import DictRepository


class DictService:
    def __init__(self, dict_repository: DictRepository):
        """
        初始化
        """
        self.__dict_repository = dict_repository

    def save_dict_info(self, dict_info: DictMetaEm, transaction: Transaction):
        """
        保存字典信息
        """
        if not dict_info.id:
            dict_meta_id = self.__dict_repository.insert_dict_meta(
                dict_meta=dict_info.to_dict_meta_model(), transaction=transaction
            )
        else:
            # 还应该做更新
            dict_meta_id = dict_info.id
        self.update_dict_data(
            dict_meta_id=dict_meta_id,
            is_tree=dict_info.is_tree,
            dict_data_list=dict_info.dict_data_list,
            transaction=transaction,
        )

    def update_dict_data(
        self,
        dict_meta_id: str,
        is_tree: bool,
        dict_data_list: List[DictDataEm],
        transaction: Transaction,
    ):
        """
        更新字典项
        """
        if is_tree:
            self.save_dict_data_of_tree_type(
                dict_meta_id=dict_meta_id, dict_data_list=dict_data_list, transaction=transaction
            )
        else:
            self.save_dict_data_of_list_type(
                dict_meta_id=dict_meta_id, dict_data_list=dict_data_list, transaction=transaction
            )

    def save_dict_data_of_tree_type(
        self,
        dict_meta_id: str,
        dict_data_list: List[DictDataEm],
        transaction: Transaction,
        parent_id: Optional[str] = None,
    ):
        """
        保存树型字典项
        """
        for dict_data in dict_data_list:
            dict_data_parent_id = self.__dict_repository.insert_dict_data(
                dict_data=dict_data.to_dict_data_model(
                    dict_meta_id=dict_meta_id, parent_id=parent_id
                ),
                transaction=transaction,
            )
            if dict_data.children:
                self.save_dict_data_of_tree_type(
                    dict_meta_id=dict_meta_id,
                    dict_data_list=[DictDataEm(**data.dict()) for data in dict_data.children],
                    transaction=transaction,
                    parent_id=dict_data_parent_id,
                )

    def save_dict_data_of_list_type(
        self, dict_meta_id: str, dict_data_list: List[DictDataEm], transaction: Transaction
    ):
        """
        保存列表型字典项
        """
        for dict_data in dict_data_list:
            self.__dict_repository.insert_dict_data(
                dict_data=dict_data.to_dict_data_model(dict_meta_id=dict_meta_id),
                transaction=transaction,
            )

    def get_dict_data_by_meta_code(self, dict_meta_code: str):
        """
        根据字典元编码获取字典数据
        """
        return self.__dict_repository.get_dict_data_by_meta_code(dict_meta_code=dict_meta_code)

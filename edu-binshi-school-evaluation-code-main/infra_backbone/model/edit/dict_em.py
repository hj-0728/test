from typing import List, Optional

from infra_basic.basic_model import BaseModel, VersionedModel

from infra_backbone.model.dict_data_model import DictDataModel
from infra_backbone.model.dict_meta_model import DictMetaModel


class DictDataBaseEm(BaseModel):
    name: str
    code: str
    value_type: str
    value: Optional[str]
    parent_id: Optional[str]
    is_editable: bool = True
    is_activated: bool = True
    seq: int = 1


class DictDataEm(DictDataBaseEm):
    """
    字典项
    """

    children: List[DictDataBaseEm] = []

    def to_dict_data_model(self, dict_meta_id: str, parent_id: Optional[str] = None):
        """
        转换成字典项model
        """
        return DictDataModel(
            dict_meta_id=dict_meta_id,
            name=self.name,
            code=self.code,
            value_type=self.value_type,
            value=self.value,
            parent_id=parent_id,
            is_editable=self.is_editable,
            is_activated=self.is_activated,
        )


class DictMetaEm(VersionedModel):
    """
    字典元
    """

    name: str
    code: str
    is_editable: bool = True
    is_activated: bool = True
    is_tree: bool = False
    dict_data_list: List[DictDataEm] = []

    def to_dict_meta_model(self):
        """
        转换成字典元model
        """
        return DictMetaModel(
            name=self.name,
            code=self.code,
            is_editable=self.is_editable,
            is_activated=self.is_activated,
            is_tree=self.is_tree,
        )

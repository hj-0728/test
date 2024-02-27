from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, Integer, String, Text, text, UniqueConstraint

from infra_backbone.entity.history.dict_data_history import DictDataHistoryEntity


class DictDataEntity(VersionedEntity):
    """
    字典数据
    """

    __tablename__ = "st_dict_data"
    __table_args__ = (
        UniqueConstraint("dict_meta_id", "code", name="uc_dict_data_meta_id_code"),
        {"comment": "字典数据"},
    )

    __history_entity__ = DictDataHistoryEntity

    dict_meta_id = Column(String(40), nullable=False, comment="字典元id", index=True)
    name = Column(String(255), nullable=False, comment="名字")
    code = Column(String(255), comment="编码", index=True)
    value_type = Column(String(255), nullable=False, comment="值类型")
    value = Column(Text, nullable=True, comment="值")
    parent_id = Column(String(40), nullable=True, comment="父id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码", server_default=text("1"))
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑", server_default=text("true"))
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))

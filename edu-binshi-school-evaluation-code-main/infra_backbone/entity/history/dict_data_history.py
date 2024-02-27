from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, Integer, String, Text, text


class DictDataHistoryEntity(HistoryEntity):
    """
    字典数据历史
    """

    __tablename__ = "st_dict_data_history"
    __table_args__ = {"comment": "字典数据历史"}

    dict_meta_id = Column(String(40), nullable=False, comment="字典元id", index=True)
    name = Column(String(255), nullable=False, comment="名字")
    code = Column(String(255), nullable=False, comment="编码", index=True)
    value_type = Column(String(255), nullable=False, comment="值类型")
    value = Column(Text, nullable=True, comment="值")
    parent_id = Column(String(40), nullable=True, comment="父id", index=True)
    seq = Column(Integer, nullable=False, comment="排序码")
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑", server_default=text("true"))
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))


Index(
    "idx_dict_data_history_time_range",
    DictDataHistoryEntity.id,
    DictDataHistoryEntity.begin_at,
    DictDataHistoryEntity.end_at.desc(),
    unique=True,
)

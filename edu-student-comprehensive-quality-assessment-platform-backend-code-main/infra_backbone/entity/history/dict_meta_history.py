"""
字典元  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String


class DictMetaHistoryEntity(HistoryEntity):
    """
    字典元历史
    """

    __tablename__ = "st_dict_meta_history"
    __table_args__ = {"comment": "字典元历史"}

    name = Column(String(255), nullable=False, comment="名字")
    code = Column(String(255), nullable=False, comment="编码")
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑")
    is_activated = Column(Boolean, nullable=False, comment="是否激活")
    is_tree = Column(Boolean, nullable=False, comment="是否树结构")


Index(
    "idx_dict_meta_history_time_range",
    DictMetaHistoryEntity.id,
    DictMetaHistoryEntity.commenced_on,
    DictMetaHistoryEntity.ceased_on.desc(),
    unique=True,
)

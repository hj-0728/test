from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.dict_meta_history import DictMetaHistoryEntity


class DictMetaEntity(VersionedEntity):
    """
    字典元
    """

    __tablename__ = "st_dict_meta"
    __table_args__ = {"comment": "字典元"}
    __history_entity__ = DictMetaHistoryEntity

    name = Column(String(255), nullable=False, comment="名字")
    code = Column(String(255), nullable=False, comment="编码", index=True, unique=True)
    is_editable = Column(Boolean, nullable=False, comment="是否可编辑", server_default=text("true"))
    is_activated = Column(Boolean, nullable=False, comment="是否激活", server_default=text("true"))
    is_tree = Column(Boolean, nullable=False, comment="是否树结构")

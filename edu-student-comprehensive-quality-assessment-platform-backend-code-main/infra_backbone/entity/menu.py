from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, Integer, String, Text

from infra_backbone.entity.history.menu_history import MenuHistoryEntity


class MenuEntity(VersionedEntity):
    """
    菜单
    """

    __tablename__ = "st_menu"
    __table_args__ = {"comment": "菜单 "}
    __history_entity__ = MenuHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    path = Column(String(255), comment="路径", nullable=False)
    icon = Column(String(2000), comment="图标")
    open_method = Column(String(255), comment="打开方式", nullable=True)
    outline = Column(Text, comment="描述")
    category = Column(String(255), comment="类型", nullable=False)
    parent_id = Column(String(40), comment="父id", nullable=True, index=True)
    seq = Column(Integer, comment="序号", nullable=False)

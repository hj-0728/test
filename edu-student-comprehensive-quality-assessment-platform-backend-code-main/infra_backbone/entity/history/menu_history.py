from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, Integer, String, Text


class MenuHistoryEntity(HistoryEntity):
    """
    菜单
    """

    __tablename__ = "st_menu_history"
    __table_args__ = {"comment": "菜单历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True, index=True)
    path = Column(String(255), comment="路径", nullable=False)
    icon = Column(String(2000), comment="图标")
    open_method = Column(String(255), comment="打开方式", nullable=True)
    outline = Column(Text, comment="描述")
    category = Column(String(255), comment="类型", nullable=False)
    parent_id = Column(String(40), comment="父id", nullable=True)
    seq = Column(Integer, comment="序号", nullable=False)


Index(
    "idx_menu_history_time_range",
    MenuHistoryEntity.id,
    MenuHistoryEntity.commenced_on,
    MenuHistoryEntity.ceased_on.desc(),
    unique=True,
)

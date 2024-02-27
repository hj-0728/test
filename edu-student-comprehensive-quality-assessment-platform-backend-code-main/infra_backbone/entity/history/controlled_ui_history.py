"""
受控UI组件  历史实体类
"""
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class ControlledUiHistoryEntity(HistoryEntity):
    """
    受控UI组件  历史实体类
    """

    __tablename__ = "st_controlled_ui_history"
    __table_args__ = {"comment": "受控UI组件"}

    ui_code = Column(String(255), nullable=False, comment="入口编码")
    name = Column(String(255), nullable=False, comment="名字")


Index(
    "idx_controlled_ui_history_time_range",
    ControlledUiHistoryEntity.id,
    ControlledUiHistoryEntity.commenced_on,
    ControlledUiHistoryEntity.ceased_on.desc(),
    unique=True,
)

from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.controlled_ui_history import ControlledUiHistoryEntity


class ControlledUiEntity(VersionedEntity):
    """
    受控UI组件
    """

    __tablename__ = "st_controlled_ui"
    __table_args__ = {"comment": "受控UI组件"}
    __history_entity__ = ControlledUiHistoryEntity

    ui_code = Column(String(255), nullable=False, comment="入口编码", index=True)
    name = Column(String(255), nullable=False, comment="名字")

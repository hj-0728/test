from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Boolean, Column, String, text

from infra_backbone.entity.history.team_category_history import TeamCategoryHistoryEntity


class TeamCategoryEntity(VersionedEntity):
    __tablename__ = "st_team_category"
    __table_args__ = {"comment": "小组分类"}
    __history_entity__ = TeamCategoryHistoryEntity

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")
    is_activated = Column(
        Boolean, nullable=False, comment="是否激活", default=True, server_default=text("true")
    )

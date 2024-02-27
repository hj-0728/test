from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Boolean, Column, Index, String, text


class TeamCategoryHistoryEntity(HistoryEntity):
    __tablename__ = "st_team_category_history"
    __table_args__ = {"comment": "小组分类(历史表)"}

    name = Column(String(255), nullable=False, comment="名称")
    code = Column(String(255), nullable=False, comment="编码")
    is_activated = Column(
        Boolean, nullable=False, comment="是否激活", default=True, server_default=text("true")
    )


Index(
    "idx_team_category_history_time_range",
    TeamCategoryHistoryEntity.id,
    TeamCategoryHistoryEntity.begin_at,
    TeamCategoryHistoryEntity.end_at.desc(),
    unique=True,
)

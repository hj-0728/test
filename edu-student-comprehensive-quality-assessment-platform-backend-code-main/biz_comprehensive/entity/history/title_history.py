from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class TitleHistoryEntity(HistoryEntity):
    """
    抬头历史
    """

    __tablename__ = "st_title_history"
    __table_args__ = {"comment": "抬头历史"}
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    assign_res_category = Column(String(255), comment="分配资源类别（TEACHER/STUDENT）", nullable=False)


Index(
    "idx_title_history_time_range",
    TitleHistoryEntity.id,
    TitleHistoryEntity.commenced_on,
    TitleHistoryEntity.ceased_on.desc(),
    unique=True,
)

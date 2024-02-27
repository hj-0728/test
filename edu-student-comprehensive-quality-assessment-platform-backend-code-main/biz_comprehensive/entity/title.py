from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from biz_comprehensive.entity.history.title_history import TitleHistoryEntity


class TitleEntity(VersionedEntity):
    """
    抬头
    """

    __tablename__ = "st_title"
    __table_args__ = {"comment": "抬头"}
    __history_entity__ = TitleHistoryEntity
    name = Column(String(255), comment="名称", nullable=False)
    code = Column(String(255), comment="编码", nullable=True)
    assign_res_category = Column(String(255), comment="分配资源类别（TEACHER/STUDENT）", nullable=False)

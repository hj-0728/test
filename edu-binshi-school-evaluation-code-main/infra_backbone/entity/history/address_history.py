from geoalchemy2 import Geography
from infra_basic.basic_entity import HistoryEntity
from sqlalchemy import Column, Index, String


class AddressHistoryEntity(HistoryEntity):
    """
    地址  历史实体类
    """

    __tablename__ = "st_address_history"
    __table_args__ = {"comment": "地址"}

    area_id = Column(String(40), nullable=False, comment="区域id", index=True)
    detail = Column(String(255), nullable=False, comment="具体地址")
    location = Column(Geography(geometry_type="POINT", srid=4326), comment="定位地址")


Index(
    "idx_address_history_time_range",
    AddressHistoryEntity.id,
    AddressHistoryEntity.begin_at,
    AddressHistoryEntity.end_at.desc(),
    unique=True,
)

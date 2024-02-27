from geoalchemy2 import Geography
from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String

from infra_backbone.entity.history.address_history import AddressHistoryEntity


class AddressEntity(VersionedEntity):
    """
    地址
    """

    __tablename__ = "st_address"
    __table_args__ = {"comment": "地址"}
    __history_entity__ = AddressHistoryEntity

    area_id = Column(String(40), nullable=False, comment="区域id", index=True)
    detail = Column(String(255), nullable=False, comment="具体地址")
    location = Column(Geography(geometry_type="POINT", srid=4326), comment="定位地址")

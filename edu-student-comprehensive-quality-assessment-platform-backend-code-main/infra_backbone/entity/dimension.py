from infra_basic.basic_entity import VersionedEntity
from sqlalchemy import Column, String, UniqueConstraint

from infra_backbone.entity.history.dimension_history import DimensionHistoryEntity


class DimensionEntity(VersionedEntity):
    """
    维度
    """

    __tablename__ = "st_dimension"

    __table_args__ = (
        UniqueConstraint(
            "organization_id", "category", name="uc_dimension_organization_id_category"
        ),
        {"comment": "维度"},
    )
    __history_entity__ = DimensionHistoryEntity

    organization_id = Column(String(40), nullable=False, comment="组织id", index=True)
    name = Column(String(255), nullable=False, comment="维度名称")
    code = Column(String(255), nullable=False, comment="维度编码", index=True)
    category = Column(String(255), nullable=False, comment="类别，用枚举处理", index=True)

from infra_basic.basic_model import VersionedModel


class TagOwnershipRelationshipModel(VersionedModel):
    """
    标签所属关系
    """

    tag_ownership_id: str
    resource_category: str
    resource_id: str
    relationship: str

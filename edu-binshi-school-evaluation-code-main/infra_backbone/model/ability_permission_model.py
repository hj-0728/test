from infra_basic.basic_model import VersionedModel


class AbilityPermissionModel(VersionedModel):
    name: str
    code: str

from infra_basic.basic_model import VersionedModel


class FilePublicLinkModel(VersionedModel):
    """
    文件的公开连接
    """

    file_id: str
    public_link: str

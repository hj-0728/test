from pydantic import BaseModel


class ZipVm(BaseModel):
    """
    待压缩文件
    """

    file_name: str
    stream_data: bytes

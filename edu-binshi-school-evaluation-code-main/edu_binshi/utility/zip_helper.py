import zipfile
from io import BytesIO
from typing import List

from edu_binshi.model.zip_model import ZipVm


def get_zip_file(file_list: List[ZipVm]) -> bytes:
    """
    将传入文件打包成一个压缩包
    @param file_list:
    @return:
    """
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zip_file:
        for file in file_list:
            zip_file.writestr(file.file_name, file.stream_data)
    memory_file.seek(0)
    return memory_file.getvalue()

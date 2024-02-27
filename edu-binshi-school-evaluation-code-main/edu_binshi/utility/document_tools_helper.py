import json
import os
import re
from typing import Dict, Tuple

import requests
from infra_basic.errors import BusinessError


class DocumentToolsHelper:
    """
    文档工具帮助类
    """

    WORD_TO_PDF_API = "http://127.0.0.1:8081"

    def __init__(self):
        """
        param app_toml_path: app.toml的路径
        """
        self.WORD_TO_PDF_API = os.environ["DOCUMENT_TOOLS_API"]

    def generate_word_with_style(self, params: Dict):
        """
        :param params {
            "cellDataList": 单元格数据列表,
            "mergeCellList": 合并单元格列表,
            "stylePosition": 样式位置dict {code: {name, code, row, col, templateFileName}},
            "maxRow": max_row,
            "maxCol": max_col,
            "waterMark": 水印文字,
            "waterMarkMode": 水印模式 默认不传，采用水平垂直居中的方式,
        }
        :return:
        """
        return self.send_bytes_res_post_request(
            url="/word-tools/generate-word-with-style",
            params=params,
        )

    def word_to_pdf(
        self,
        file: Tuple[str, bytes],
        params: Dict = None,
    ):
        """
        :param file (aaa.docx, word文件bytes)
        :param params {
            "waterMark": 水印文字,
            "waterMarkMode": 水印模式 默认不传，采用水平垂直居中的方式,
        }
        :return:
        """
        return self.send_bytes_res_post_request(
            url="/word-tools/word-to-pdf",
            params=params,
            files={"file": file},
        )

    def send_bytes_res_post_request(
        self,
        url: str,
        params: Dict = None,
        files: Dict[str, Tuple[str, bytes]] = None,
    ):
        """
        发送返回字节流的post请求
        """
        url = f"{self.WORD_TO_PDF_API}{url}"
        headers = {"Content-Type": "application/json"}
        result = requests.post(url=url, json=params)
        if files:
            result = requests.post(
                url=url,
                files=files,
                data=json.dumps(params, ensure_ascii=False).encode("utf-8") if params else None,
                headers=None if files else headers,
            )
        content_type = result.headers.get("Content-Type", None)
        content = result.content
        if content_type == "application/json":
            error = content.decode("utf-8")
            raise BusinessError(error)
        elif content_type == "application/octet-stream":
            content_disposition = result.headers.get("Content-Disposition", None)
            if content_disposition:
                file_name = self.get_file_name_from_content_disposition(content_disposition)
                return (
                    content,
                    file_name,
                )
            raise BusinessError("未获取Content-Disposition信息")
        else:
            raise BusinessError("其他错误")

    @staticmethod
    def get_file_name_from_content_disposition(content_disposition):
        """
        从Content-Disposition中获取文件名
        :param content_disposition:
        :return: 文件名
        """
        pattern = r"filename=([^;]+)"
        match = re.search(pattern, content_disposition)
        if match:
            return match.group(1).strip('"')
        else:
            return None

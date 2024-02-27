"""
word 转 pdf 助手
"""

import json
import os

import requests
from infra_basic.errors import BusinessError


def doc2pdf(files) -> bytes:
    """
    word 转 pdf
    :return:
    """
    word_to_pdf_api = os.environ.get("document_tools_api", "http://127.0.0.1:8080")
    url = f"{word_to_pdf_api}/word-to-pdf"
    result = requests.post(url, files=files, data={'version': ""})
    content_type = result.headers.get("Content-Type", None)
    content = result.content
    if content_type == "application/json":
        content_json = json.loads(content)
        if content_json["code"] == 500:
            message = content_json.get("messages", [])
            raise BusinessError(message)
    return content

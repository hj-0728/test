"""
服务器帮助类
"""

from flask import request


def prepare_url(url: str = "") -> str:
    """
    构建url，主要是为了解决反向代理后的url，配合ReverseProxyApp使用
    :param url: 原始url
    :return: 根据反向代理来构造新的url
    """
    if "SCRIPT_NAME" in request.environ:
        return "{0}{1}".format(request.environ["SCRIPT_NAME"], url)
    return url


def get_request_user_agent() -> str:
    return request.headers.get("User-Agent")


def get_request_ip() -> str:
    """
    从request中获取ip地址，因为被反向代理后取remote_addr是不对的
    :return:
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr

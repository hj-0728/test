# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import socket
import struct

from infra_dingtalk.dingtalk.core.utils import byte2int, random_string, to_binary, to_text
from infra_dingtalk.dingtalk.crypto.pkcs7 import PKCS7Encoder

try:
    from infra_dingtalk.dingtalk.crypto.cryptography import DingTalkCipher
except ImportError:
    try:
        from infra_dingtalk.dingtalk.crypto.pycrypto import DingTalkCipher
    except ImportError:
        raise Exception("You must install either cryptography or PyCrypto!")


class BasePrpCrypto(object):
    def __init__(self, key):
        self.cipher = DingTalkCipher(key)

    def get_random_string(self):
        return random_string(16)

    def _encrypt(self, text, _id):
        text = to_binary(text)
        tmp_list = []
        tmp_list.append(to_binary(self.get_random_string()))
        length = struct.pack(b"I", socket.htonl(len(text)))
        tmp_list.append(length)
        tmp_list.append(text)
        tmp_list.append(to_binary(_id))

        text = b"".join(tmp_list)
        text = PKCS7Encoder.encode(text)

        ciphertext = to_binary(self.cipher.encrypt(text))
        return base64.b64encode(ciphertext)

    def _decrypt(self, text, _id, exception=None):
        text = to_binary(text)
        plain_text = self.cipher.decrypt(base64.b64decode(text))
        padding = byte2int(plain_text[-1])
        content = plain_text[16:-padding]
        xml_length = socket.ntohl(struct.unpack(b"I", content[:4])[0])
        xml_content = to_text(content[4 : xml_length + 4])
        from_id = to_text(content[xml_length + 4 :])
        if from_id != _id:
            exception = exception or Exception
            raise exception()
        return xml_content

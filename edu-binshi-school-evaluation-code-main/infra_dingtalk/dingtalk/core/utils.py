# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import hashlib
import json
import random
import string

import six


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access."""

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value


class DingTalkSigner(object):
    """DingTalk data signer"""

    def __init__(self, delimiter=b""):
        self._data = []
        self._delimiter = to_binary(delimiter)

    def add_data(self, *args):
        """Add data to signer"""
        for data in args:
            self._data.append(to_binary(data))

    @property
    def signature(self):
        """Get data signature"""
        self._data.sort()
        str_to_sign = self._delimiter.join(self._data)
        return hashlib.sha1(str_to_sign).hexdigest()


def to_text(value, encoding="utf-8"):
    """Convert value to unicode, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return ""
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding="utf-8"):
    """Convert value to binary string, default encoding is utf-8

    :param value: Value to be converted
    :param encoding: Desired encoding
    """
    if not value:
        return b""
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return to_text(value).encode(encoding)


def random_string(length=16):
    rule = string.ascii_letters + string.digits
    rand_list = random.sample(rule, length)
    return "".join(rand_list)


def byte2int(c):
    if six.PY2:
        return ord(c)
    return c


def json_loads(s, object_hook=ObjectDict, **kwargs):
    return json.loads(s, object_hook=object_hook, **kwargs)

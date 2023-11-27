#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_fields.captcha module

This module provides components for Google reCaptcha support.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_fields.interfaces import CAPTCHA_MANAGER_INFO_KEY, ICaptchaInfo, ICaptchaManagerInfo, \
    ICaptchaManagerTarget, ICaptchaTarget
from pyams_security.interfaces.names import UNCHANGED_PASSWORD
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.traversing import get_parent


@factory_config(ICaptchaManagerInfo)
class CaptchaManagerInfo(Persistent, Contained):
    """Captcha manager persistent info"""

    use_captcha = FieldProperty(ICaptchaManagerInfo['use_captcha'])
    default_captcha_client_key = FieldProperty(
        ICaptchaManagerInfo['default_captcha_client_key'])
    default_captcha_server_key = FieldProperty(
        ICaptchaManagerInfo['default_captcha_server_key'])
    use_proxy = FieldProperty(ICaptchaManagerInfo['use_proxy'])
    proxy_proto = FieldProperty(ICaptchaManagerInfo['proxy_proto'])
    proxy_host = FieldProperty(ICaptchaManagerInfo['proxy_host'])
    proxy_port = FieldProperty(ICaptchaManagerInfo['proxy_port'])
    proxy_username = FieldProperty(ICaptchaManagerInfo['proxy_username'])
    _proxy_password = FieldProperty(ICaptchaManagerInfo['proxy_password'])
    proxy_only_from = FieldProperty(ICaptchaManagerInfo['proxy_only_from'])

    @property
    def proxy_password(self):
        """Proxy password getter"""
        return self._proxy_password

    @proxy_password.setter
    def proxy_password(self, value):
        """Proxy password setter"""
        if value == UNCHANGED_PASSWORD:
            return
        self._proxy_password = value

    def get_captcha_settings(self):
        """Captcha settings getter"""
        return {
            'use_captcha': self.use_captcha,
            'client_key': self.default_captcha_client_key if self.use_captcha else None,
            'server_key': self.default_captcha_server_key if self.use_captcha else None
        }

    def get_proxy_url(self, request):
        """Proxy URL getter"""
        if not self.use_proxy:
            return None
        # check selected domains names
        if self.proxy_only_from:
            domains = map(str.strip, self.proxy_only_from.split(','))
            if request.host not in domains:
                return None
        return '{}://{}{}:{}/'.format(self.proxy_proto,
                                      '{}{}{}@'.format(self.proxy_username,
                                                       ':' if self.proxy_password else '',
                                                       self.proxy_password or '')
                                      if self.proxy_username else '',
                                      self.proxy_host,
                                      self.proxy_port)


@adapter_config(required=ICaptchaManagerTarget,
                provides=ICaptchaManagerInfo)
def captcha_manager_info(context):
    """Captcha manager info factory"""
    return get_annotation_adapter(context, CAPTCHA_MANAGER_INFO_KEY,
                                  ICaptchaManagerInfo)


@factory_config(ICaptchaInfo)
class CaptchaInfo(Persistent, Contained):
    """Captcha persistent info"""

    override_captcha = FieldProperty(ICaptchaInfo['override_captcha'])
    captcha_client_key = FieldProperty(ICaptchaInfo['captcha_client_key'])
    captcha_server_key = FieldProperty(ICaptchaInfo['captcha_server_key'])

    def get_captcha_settings(self):
        """Captcha settings getter"""
        if self.override_captcha:
            return {
                'use_captcha': bool(self.captcha_client_key),
                'client_key': self.captcha_client_key,
                'server_key': self.captcha_server_key
            }
        target = get_parent(self, ICaptchaManagerTarget)
        if target is not None:
            return ICaptchaManagerInfo(target).get_captcha_settings()
        return {}


@adapter_config(required=ICaptchaTarget,
                provides=ICaptchaInfo)
def captcha_info(context):
    """Captcha info"""
    return get_annotation_adapter(context, CAPTCHA_MANAGER_INFO_KEY,
                                  ICaptchaInfo)

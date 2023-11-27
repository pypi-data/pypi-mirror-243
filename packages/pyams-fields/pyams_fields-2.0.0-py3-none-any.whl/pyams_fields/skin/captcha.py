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

"""PyAMS_fields.skin.captcha module

This module provides components for Google reCaptcha v3 support.
"""

__docformat__ = 'restructuredtext'

from zope.interface import Interface

from pyams_fields.interfaces import ICaptchaInfo, IFormFieldContainerTarget
from pyams_fields.skin import IFormFieldContainerInputForm
from pyams_form.interfaces.form import IForm
from pyams_layer.interfaces import IPyAMSLayer, IPyAMSUserLayer
from pyams_skin.interfaces.viewlet import IFormHeaderViewletManager
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.tales import ITALESExtension
from pyams_viewlet.viewlet import Viewlet, viewlet_config


def get_captcha_settings(context):
    """Get captcha settings from context"""
    captcha_info = ICaptchaInfo(context, None)
    if captcha_info is None:
        return None
    settings = captcha_info.get_captcha_settings()
    if not settings.get('use_captcha'):
        return None
    return settings


@viewlet_config(name='recaptcha',
                context=IFormFieldContainerTarget, layer=IPyAMSUserLayer,
                view=IFormFieldContainerInputForm,
                manager=IFormHeaderViewletManager)
@template_config(template='templates/recaptcha.pt', layer=IPyAMSUserLayer)
class FormCaptchaViewlet(Viewlet):
    """Form captcha viewlet"""

    def __new__(cls, context, request, view, manager):
        if get_captcha_settings(context) is None:
            return None
        return Viewlet.__new__(cls)

    @property
    def client_key(self):
        """Captcha client key"""
        return get_captcha_settings(self.context).get('client_key')


@adapter_config(name='recaptcha.client_key',
                required=(Interface, IPyAMSLayer, IForm),
                provides=ITALESExtension)
class CaptchaClientKeyTALESExtension(ContextRequestViewAdapter):
    """Captcha client key TALES extension"""

    def render(self, context=None):
        """Render extension"""
        if context is None:
            context = self.request.context
        settings = get_captcha_settings(context)
        if settings is None:
            return None
        return settings.get('client_key')

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

"""PyAMS_fields.zmi.captcha module

Management interface components for captcha support.
"""

__docformat__ = 'restructuredtext'

from pyramid.events import subscriber
from zope.interface import Invalid

from pyams_fields.interfaces import ICaptchaInfo, ICaptchaManagerInfo, ICaptchaManagerTarget, \
    ICaptchaTarget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IDataExtractedEvent, IGroup
from pyams_utils.adapter import adapter_config
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm


__docformat__ = 'restructuredtext'

from pyams_fields import _


@adapter_config(name='base-captcha-settings',
                required=(ICaptchaManagerTarget, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
class CaptchaManagerBaseSettingsGroup(FormGroupChecker):
    """Captcha manager base settings group"""

    fields = Fields(ICaptchaManagerInfo).select('use_captcha',
                                                'default_captcha_client_key',
                                                'default_captcha_server_key')


@subscriber(IDataExtractedEvent, form_selector=CaptchaManagerBaseSettingsGroup)
def extract_captcha_manager_settings(event):
    """Extract captcha settings"""
    data = event.data
    if data.get('use_captcha'):
        if not (data.get('default_captcha_client_key') and
                data.get('default_captcha_server_key')):
            event.form.widgets.errors += (Invalid(_("You must define client and server keys "
                                                    "to use a captcha")),)


@adapter_config(name='captcha-proxy-settings',
                required=(ICaptchaManagerTarget, IAdminLayer, CaptchaManagerBaseSettingsGroup),
                provides=IGroup)
class CaptchaManagerProxySettingsEditFormGroup(FormGroupChecker):
    """Captcha manager proxy settings edit form"""

    fields = Fields(ICaptchaManagerInfo).select('use_proxy', 'proxy_proto', 'proxy_host',
                                                'proxy_port', 'proxy_username',
                                                'proxy_password', 'proxy_only_from')


@subscriber(IDataExtractedEvent, form_selector=CaptchaManagerProxySettingsEditFormGroup)
def extract_captcha_manager_proxy_settings(event):
    """Extract captcha proxy settings"""
    parent_data, parent_errors = event.form.parent_form.extract_data(set_errors=False,
                                                                     notify=False)
    if parent_data.get('use_captcha'):
        data = event.data
        if data.get('use_proxy') and \
                not (data.get('proxy_proto') and
                     data.get('proxy_host') and
                     data.get('proxy_port')):
            event.form.widgets.errors += (Invalid(_("You must define protocol, host name "
                                                    "and port be able to use a proxy!")),)


#
# Custom captcha settings
#

@adapter_config(name='captcha-settings',
                required=(ICaptchaTarget, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
class CaptchaSettingsEditFormGroup(FormGroupChecker):
    """Captcha settings edit form"""

    fields = Fields(ICaptchaInfo)

    weight = 10


@subscriber(IDataExtractedEvent, form_selector=CaptchaSettingsEditFormGroup)
def extract_captcha_settings(event):
    """Extract captcha settings"""
    data = event.data
    if data.get('override_captcha'):
        if bool(data.get('captcha_client_key')) ^ bool(data.get('captcha_server_key')):
            event.form.widgets.errors += (Invalid(_("You must redefine both client and server "
                                                    "keys, or none or them to disable "
                                                    "captcha for this form!")),)

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

"""PyAMS_fields.skin.rgpd module

This module provides an field widget for RGPD consent.
"""

__docformat__ = 'restructuredtext'

from pyams_form.browser.checkbox import SingleCheckBoxWidget
from pyams_form.interfaces import INPUT_MODE
from pyams_form.template import widget_template_config
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IPyAMSUserLayer


@widget_template_config(mode=INPUT_MODE,
                        template='templates/rgpd-consent-widget.pt',
                        layer=IPyAMSUserLayer)
class RGPDConsentWidget(SingleCheckBoxWidget):
    """RGPD consent widget"""


def RGPDConsentFieldWidget(field, request):
    """RGPD consent field widget factory"""
    return FieldWidget(field, RGPDConsentWidget(request))

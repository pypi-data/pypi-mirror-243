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

"""PyAMS_fields.zmi.handler module

Management interface components for form handlers support.
"""

from zope.interface import implementer

from pyams_fields.zmi.interfaces import IFormHandlersSettingsGroup
from pyams_fields.interfaces import IFormHandlersInfo, IFormHandlersTarget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IGroup
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_zmi.form import FormGroupSwitcher
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm


__docformat__ = 'restructuredtext'

from pyams_fields import _


@adapter_config(name='handlers-settings',
                required=(IFormHandlersTarget, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
@implementer(IFormHandlersSettingsGroup)
class FormHandlersSettingsGroup(FormGroupSwitcher):
    """Form handlers settings edit form"""

    legend = _("Form handlers")

    fields = Fields(IFormHandlersInfo)

    weight = 40

    def update_widgets(self, prefix=None, use_form_mode=True):
        super().update_widgets(prefix, use_form_mode)
        handlers = self.widgets.get('handlers')
        if handlers is not None:
            translate = self.request.localizer.translate
            handlers.placeholder = translate(_("No selected handler"))


@adapter_config(required=(IFormHandlersTarget, IAdminLayer, IPropertiesEditForm),
                provided=IAJAXFormRenderer)
class FormHandlersEditFormRenderer(ContextRequestViewAdapter):
    """Form handlers edit form renderer"""

    def render(self, changes):
        """Form renderer"""
        if (changes is None) or \
                ('handlers' not in changes.get(IFormHandlersInfo, ())):
            return None
        return {
            'status': 'redirect'
        }

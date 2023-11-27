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

"""PyAMS_fields.zmi.rgpd module

Management interface components for RGPD support.
"""

__docformat__ = 'restructuredtext'

from pyramid.events import subscriber
from zope.interface import Invalid

from pyams_fields.interfaces import IRGPDInfo, IRGPDTarget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_template.template import template_config
from pyams_utils.adapter import adapter_config
from pyams_utils.dict import boolean_dict
from pyams_viewlet.viewlet import ViewContentProvider
from pyams_zmi.form import FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.form import IPropertiesEditForm

from pyams_fields import _


@template_config(template='templates/rgpd-warning.pt', layer=IPyAMSLayer)
class RGPDWarningNotice(ViewContentProvider):
    """RGPD user warning notice"""


@template_config(template='templates/rgpd-user-rights.pt', layer=IPyAMSLayer)
class RGPDUserRightsNotice(ViewContentProvider):
    """RGPD user rights notice"""


@adapter_config(name='rgpd-settings',
                required=(IRGPDTarget, IAdminLayer, IPropertiesEditForm),
                provides=IGroup)
class RGPDInfoEditFormGroup(FormGroupChecker):
    """RGPD info edit form group"""

    fields = Fields(IRGPDInfo)

    weight = 30

    def update_widgets(self, prefix=None, use_form_mode=True):
        """Widgets update"""
        super().update_widgets(prefix, use_form_mode)
        warning = self.widgets.get('rgpd_warning')
        if warning is not None:
            warning.suffix = notice = RGPDWarningNotice(self.context, self.request, self.parent_form)
            notice.update()
        rights = self.widgets.get('rgpd_user_rights')
        if rights is not None:
            rights.suffix = notice = RGPDUserRightsNotice(self.context, self.request, self.parent_form)
            notice.update()


@subscriber(IDataExtractedEvent, form_selector=RGPDInfoEditFormGroup)
def extract_rgpd_info(event):
    """Extract RGPD info"""
    data = event.data
    if data.get('rgpd_consent') and \
            not (boolean_dict(data.get('rgpd_warning')) and
                 boolean_dict(data.get('rgpd_user_rights'))):
        event.form.widgets.errors += (Invalid(_("You must define RGPD consent text and user rights to "
                                                "enable RGPD consent!")),)

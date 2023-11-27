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

"""PyAMS_fields.rgpd module

This module provides base components for RGPD support.
"""

__docformat__ = 'restructuredtext'

from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_fields.interfaces import IRGPDInfo, IRGPDTarget, RGPD_INFO_KEY
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config


@factory_config(IRGPDInfo)
class RGPDInfo(Persistent, Contained):
    """RGPD info persistent class"""

    rgpd_consent = FieldProperty(IRGPDInfo['rgpd_consent'])
    rgpd_warning = FieldProperty(IRGPDInfo['rgpd_warning'])
    rgpd_user_rights = FieldProperty(IRGPDInfo['rgpd_user_rights'])


@adapter_config(required=IRGPDTarget,
                provides=IRGPDInfo)
def rgpd_info(context):
    """RGPD info getter"""
    return get_annotation_adapter(context, RGPD_INFO_KEY, IRGPDInfo)

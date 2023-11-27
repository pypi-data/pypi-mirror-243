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

"""PyAMS_fields.zmi.interfaces module

"""

from zope.interface import Interface


__docformat__ = 'restructuredtext'


class IFormFieldsTable(Interface):
    """Form fields table marker interface"""


class IFormFieldAddForm(Interface):
    """Form field add form marker interface"""


class IFormHandlersSettingsGroup(Interface):
    """Form handlers settings group marker interface"""

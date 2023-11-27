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

"""PyAMS_fields.zmi.container module

"""

from pyramid.interfaces import IView
from pyramid.view import view_config
from zope.interface import implementer

from pyams_fields.interfaces import IFormFieldContainer, IFormFieldContainerTarget
from pyams_fields.zmi.interfaces import IFormFieldsTable
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_table.interfaces import IColumn, IValues
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.factory import factory_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.helper.container import delete_container_element, switch_element_attribute
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.viewlet import IPropertiesMenu
from pyams_zmi.table import ContentTypeColumn, NameColumn, ReorderColumn, SortableTable, TableAdminView, \
    TrashColumn, VisibilityColumn
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_fields import _


@viewlet_config(name='form-fields.menu',
                context=IFormFieldContainerTarget, layer=IAdminLayer,
                manager=IPropertiesMenu, weight=95,
                permission=VIEW_SYSTEM_PERMISSION)
class FormFieldsContainerMenu(NavigationMenuItem):
    """Form fields container menu"""

    label = _("Form fields")
    href = '#form-fields.html'


@factory_config(IFormFieldsTable)
@implementer(IView)
class FormFieldsTable(SortableTable):
    """Form fields container table"""

    container_class = IFormFieldContainer

    display_if_empty = True


@adapter_config(required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IValues)
class FormFieldsTableValues(ContextRequestViewAdapter):
    """Form fields table values"""

    @property
    def values(self):
        """Form fields container values getter"""
        yield from IFormFieldContainer(self.context).values()


@adapter_config(name='reorder',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsReorderColumn(ReorderColumn):
    """Form fields reorder column"""


@view_config(name='reorder.json',
             context=IFormFieldContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def reorder_form_fields_table(request):
    """Reorder form fields"""
    order = request.params.get('order').split(';')
    IFormFieldContainer(request.context).updateOrder(order)
    return {
        'status': 'success',
        'closeForm': False
    }


@adapter_config(name='visible',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsVisibleColumn(VisibilityColumn):
    """Form fields table visible column"""


@view_config(name='switch-visible-item.json',
             context=IFormFieldContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def switch_visible_item(request):
    """Switch visible item"""
    return switch_element_attribute(request)


@adapter_config(name='icon',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsIconColumn(ContentTypeColumn):
    """Form fields table icon column"""


@adapter_config(name='label',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsLabelColumn(NameColumn):
    """Form fields table label column"""

    i18n_header = _("Public label")


@adapter_config(name='name',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsNameColumn(NameColumn):
    """Form fields table name column"""

    i18n_header = _("Field name")
    weight = 20

    def get_value(self, obj):
        """Field name getter"""
        return obj.name


@adapter_config(name='trash',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class AssociationsTrashColumn(TrashColumn):
    """Form fields table trash column"""


@view_config(name='delete-element.json',
             context=IFormFieldContainer, request_type=IPyAMSLayer,
             renderer='json', xhr=True)
def delete_form_field(request):
    """Delete form field"""
    return delete_container_element(request)


@pagelet_config(name='form-fields.html',
                context=IFormFieldContainerTarget, layer=IPyAMSLayer)
class FormFieldsContainerView(TableAdminView):
    """Form fields container view"""

    title = _("Form fields")

    table_class = IFormFieldsTable
    table_label = _("Form fields list")

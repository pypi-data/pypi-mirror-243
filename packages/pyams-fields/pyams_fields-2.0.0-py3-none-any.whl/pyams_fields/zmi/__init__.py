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

"""PyAMS_fields.zmi module

"""

from pyramid.events import subscriber
from zope.copy import copy
from zope.interface import Interface, Invalid, implementer

from pyams_fields.interfaces import IFormField, IFormFieldContainer, IFormFieldContainerTarget
from pyams_fields.zmi.interfaces import IFormFieldAddForm, IFormFieldsTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_security.interfaces.base import FORBIDDEN_PERMISSION, VIEW_SYSTEM_PERMISSION
from pyams_skin.viewlet.actions import ContextAddAction
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.traversing import get_parent
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_add_callback, \
    get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer, IObjectHint, IObjectIcon, IObjectLabel
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import ActionColumn, TableElementEditor
from pyams_zmi.utils import get_object_label


__docformat__ = 'restructuredtext'

from pyams_fields import _


@viewlet_config(name='add-form-field.action',
                context=IFormFieldContainerTarget, layer=IAdminLayer, view=IFormFieldsTable,
                manager=IToolbarViewletManager, weight=20)
class FormFieldAddAction(ContextAddAction):
    """Form field add action"""

    label = _("Add form field")
    href = 'add-form-field.html'

    def __new__(cls, context, request, view, manager):
        """Permission getter"""
        checker = IViewContextPermissionChecker(context, None)
        if checker is not None:
            permission = checker.edit_permission
            if permission and not request.has_permission(permission, context=context):
                return None
        return ContextAddAction.__new__(cls)


@ajax_form_config(name='add-form-field.html',
                  context=IFormFieldContainerTarget, layer=IPyAMSLayer)
@implementer(IFormFieldAddForm)
class FormFieldAddForm(AdminModalAddForm):
    """Form field add form"""

    def __new__(cls, context, request):
        checker = IViewContextPermissionChecker(context, None)
        if checker is not None:
            permission = checker.edit_permission
            if permission and not request.has_permission(permission, context=context):
                return None
        return AdminModalAddForm.__new__(cls)

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        return '<small>{}</small><br />{}'.format(
            get_object_label(self.context, self.request),
            translate(_("Add new form field")))

    legend = _("New form field properties")

    fields = Fields(IFormField).omit('__name__', '__parent__', 'visible')

    content_factory = IFormField

    def add(self, obj):
        """Add form field to container"""
        IFormFieldContainer(self.context)[obj.name] = obj


@subscriber(IDataExtractedEvent, form_selector=IFormFieldAddForm)
def form_field_add_form_data_extract(event):
    """Form field add form data extraction"""
    name = event.data['name'] or ''
    target = get_parent(event.form.get_content(), IFormFieldContainerTarget)
    if target is not None:
        field = IFormFieldContainer(target).get(name)
        if field is not None:
            event.form.widgets.errors += (Invalid(_("Another form field already exists with "
                                                    "this name!")),)


@adapter_config(required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldAddForm),
                provides=IAJAXFormRenderer)
class FormFieldAddFormRenderer(ContextRequestViewAdapter):
    """Form field add form renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:
            return None
        return {
            'status': 'success',
            'callbacks': [
                get_json_table_row_add_callback(self.context, self.request,
                                                IFormFieldsTable, changes)
            ]
        }


@adapter_config(required=(IFormField, IAdminLayer, Interface),
                provides=IObjectLabel)
def form_field_label(context, request, view):
    """Form field label getter"""
    i18n = II18n(context)
    return i18n.query_attribute('label', request=request)


@adapter_config(required=(IFormField, IAdminLayer, Interface),
                provides=IObjectIcon)
def form_field_icon(context, request, view):
    """Form field icon getter"""
    factory = context.get_field_factory()
    return factory.icon_class if factory is not None else None


@adapter_config(required=(IFormField, IAdminLayer, Interface),
                provides=IObjectHint)
def form_field_hint(context, request, view):
    """Form field hint getter"""
    factory = context.get_field_factory()
    return request.localizer.translate(factory.label) if factory is not None else None


@adapter_config(required=(IFormField, IAdminLayer, IFormFieldsTable),
                provides=ITableElementEditor)
class FormFieldElementEditor(TableElementEditor):
    """Form field element editor"""


@ajax_form_config(name='properties.html',
                  context=IFormField, layer=IPyAMSLayer)
class FormFieldEditForm(AdminModalEditForm):
    """Form field properties edit form"""

    legend = _("Form field properties")

    fields = Fields(IFormField).omit('__name__', '__parent__', 'visible')

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        parent = get_parent(self.context, IFormFieldContainerTarget)
        return '<small>{}</small><br />{}'.format(
            get_object_label(parent, self.request),
            translate(_("Form field: {}")).format(get_object_label(self.context, self.request)))

    def update_widgets(self, prefix=None):  # pylint: disable=unused-argument
        """Widgets update"""
        super().update_widgets()
        name = self.widgets.get('name')
        if name is not None:
            name.mode = DISPLAY_MODE


@adapter_config(required=(IFormField, IAdminLayer, FormFieldEditForm),
                provides=IAJAXFormRenderer)
class FormFieldEditFormRenderer(ContextRequestViewAdapter):
    """Form film edit form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        target = get_parent(self.context, IFormFieldContainerTarget)
        return {
            'status': self.view.success_message,
            'callbacks': [
                get_json_table_row_refresh_callback(target, self.request,
                                                    IFormFieldsTable, self.context)
            ]
        }


@adapter_config(name='clone',
                required=(IFormFieldContainerTarget, IAdminLayer, IFormFieldsTable),
                provides=IColumn)
class FormFieldsCloneColumn(ActionColumn):
    """Form fields table clone column"""

    hint = _("Clone field")
    icon_class = 'far fa-clone'

    href = 'clone-form-field.html'
    weight = 100

    @property
    def permission(self):
        """Permission getter"""
        checker = IViewContextPermissionChecker(self.context, None)
        if checker is not None:
            permission = checker.edit_permission
            if permission and not self.request.has_permission(permission, context=self.context):
                return FORBIDDEN_PERMISSION
        return VIEW_SYSTEM_PERMISSION


@ajax_form_config(name='clone-form-field.html',
                  context=IFormField, layer=IPyAMSLayer)
@implementer(IFormFieldAddForm)
class FormFieldCloneForm(AdminModalAddForm):
    """Portal template clone form"""

    @property
    def title(self):
        """Form title getter"""
        translate = self.request.localizer.translate
        parent = get_parent(self.context, IFormFieldContainerTarget)
        return '<small>{}</small><br />{}'.format(
            get_object_label(parent, self.request),
            translate(_("Form field: {}")).format(get_object_label(self.context, self.request)))

    legend = _("Clone form field")

    fields = Fields(IFormField).select('name')

    def create(self, data):
        """Create new form field by copying context"""
        return copy(self.context)

    def add(self, obj):
        """Add new form field to container"""
        IFormFieldContainer(self.context.__parent__)[obj.name] = obj


@adapter_config(required=(IFormField, IAdminLayer, FormFieldCloneForm),
                provides=IAJAXFormRenderer)
class FormFieldCloneFormRenderer(ContextRequestViewAdapter):
    """Form field form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        target = get_parent(self.context, IFormFieldContainerTarget)
        return {
            'callbacks': [
                get_json_table_row_add_callback(target, self.request,
                                                IFormFieldsTable, changes)
            ]
        }

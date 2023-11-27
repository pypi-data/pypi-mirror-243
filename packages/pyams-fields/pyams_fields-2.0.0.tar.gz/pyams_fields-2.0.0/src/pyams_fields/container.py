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

"""PyAMS_fields.container module

This module defines fields container class.
"""

__docformat__ = 'restructuredtext'

from zope.container.ordered import OrderedContainer
from zope.location.interfaces import ISublocations
from zope.traversing.interfaces import ITraversable

from pyams_fields.interfaces import IFormFieldContainer, IFormFieldContainerTarget, \
    IFormFieldFactory, PYAMS_FIELDS_CONTAINER_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry


@factory_config(IFormFieldContainer)
class FormFieldContainer(OrderedContainer):
    """Form fields container"""

    def get_fields(self):
        """Get iterator over current schema fields"""
        registry = get_pyramid_registry()
        for field in self.values():
            if not field.visible:
                continue
            factory = registry.queryUtility(IFormFieldFactory, name=field.field_type)
            if factory is not None:
                yield factory.get_schema_field(field)

    def find_fields(self, factory: str):
        """Find fields matching given factory"""
        for field in self.values():
            if not field.visible:
                continue
            if field.field_type == factory:
                yield field


@adapter_config(required=IFormFieldContainerTarget,
                provides=IFormFieldContainer)
def form_field_container(context):
    """Form fields container factory"""
    return get_annotation_adapter(context, PYAMS_FIELDS_CONTAINER_KEY,
                                  IFormFieldContainer, name='++fields++')


@adapter_config(name='fields',
                required=IFormFieldContainerTarget,
                provides=ITraversable)
class FormFieldContainerNamespace(ContextAdapter):
    """Form fields container ++fields++ namespace"""

    def traverse(self, name, furtherpath=None):  # pylint: disable=unused-argument
        """Form fields traverser"""
        container = IFormFieldContainer(self.context)
        if name:
            return container.get(name)
        return container


@adapter_config(name='fields',
                required=IFormFieldContainerTarget,
                provides=ISublocations)
class FormFieldsContainerSublocations(ContextAdapter):
    """Form fields container sub-locations adapter"""

    def sublocations(self):
        """Sub-locations iterator"""
        yield from IFormFieldContainer(self.context).values()

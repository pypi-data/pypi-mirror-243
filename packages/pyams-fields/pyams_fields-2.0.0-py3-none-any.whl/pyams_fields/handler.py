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

"""PyAMS_fields.handler module

This module provides base components for form handlers support.
"""

from persistent import Persistent
from pyramid.interfaces import IView
from zope.container.contained import Contained
from zope.interface import alsoProvides, noLongerProvides
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.traversing.interfaces import ITraversable

from pyams_fields.interfaces import FORM_HANDLERS_INFO_KEY, FORM_HANDLERS_VOCABULARY, IFormHandler, IFormHandlerInfo, \
    IFormHandlersInfo, IFormHandlersTarget
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import ContextAdapter, adapter_config, get_adapter_weight, get_annotation_adapter
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config


__docformat__ = 'restructuredtext'


@factory_config(IFormHandlersInfo)
class FormHandlersInfo(Persistent, Contained):
    """Form handlers persistent info"""

    _auth_only = FieldProperty(IFormHandlersInfo['auth_only'])
    submit_label = FieldProperty(IFormHandlersInfo['submit_label'])
    submit_message = FieldProperty(IFormHandlersInfo['submit_message'])
    submission_id_format = FieldProperty(IFormHandlersInfo['submission_id_format'])
    _handlers = FieldProperty(IFormHandlersInfo['handlers'])

    @property
    def auth_only(self):
        """Authenticated-only getter"""
        return self._auth_only

    @auth_only.setter
    def auth_only(self, value):
        """Authenticated-only setter"""
        if value == self._auth_only:
            return
        self._auth_only = value

    @property
    def handlers(self):
        """Handlers getter"""
        return self._handlers

    @handlers.setter
    def handlers(self, value):
        """Handlers setter"""
        old_handlers = self._handlers or []
        removed = set(old_handlers) - set(value or ())
        for handler_name in removed:
            handler = self.query_handler(handler_name)
            if handler is None:
                continue
            if handler.target_interface is not None:
                noLongerProvides(self, handler.target_interface)
        added = set(value or ()) - set(old_handlers)
        for handler_name in added:
            handler = self.query_handler(handler_name)
            if handler is None:
                continue
            if handler.target_interface is not None:
                alsoProvides(self, handler.target_interface)
        self._handlers = value

    @staticmethod
    def query_handler(name=None):
        """Handler getter"""
        if name is None:
            return None
        registry = get_pyramid_registry()
        return registry.queryUtility(IFormHandler, name=name)


@adapter_config(required=IFormHandlersTarget,
                provides=IFormHandlersInfo)
def form_handlers_info(context):
    """Form handlers information getter"""
    return get_annotation_adapter(context, FORM_HANDLERS_INFO_KEY,
                                  IFormHandlersInfo,
                                  name='++handlers++')


@adapter_config(name='handlers',
                required=IFormHandlersTarget,
                provides=ITraversable)
class FormHandlersTraverser(ContextAdapter):
    """Form handlers traverser"""

    def traverse(self, name, furtherpath=None):
        """Form handler traverser"""
        return IFormHandlersInfo(self.context)


@vocabulary_config(name=FORM_HANDLERS_VOCABULARY)
class FormHandlersVocabulary(SimpleVocabulary):
    """Form handlers vocabulary"""

    interface = IFormHandler

    def __init__(self, context, **kw):
        registry = get_pyramid_registry()
        terms = [
            SimpleTerm(name, title=util.label)
            for name, util in sorted(registry.getUtilitiesFor(self.interface),
                                     key=get_adapter_weight)
        ]
        super().__init__(terms)


@adapter_config(name='handler',
                required=IFormHandlersInfo,
                provides=ITraversable)
class FormHandlerInfoTraverser(ContextAdapter):
    """Form handler info traverser"""

    def traverse(self, name, furtherpath=None):
        """Form handler traverser"""
        registry = get_pyramid_registry()
        handlers = IFormHandlersInfo(self.context)
        return registry.queryAdapter(handlers, IFormHandlerInfo,
                                     name=name)


@adapter_config(required=(IFormHandlerInfo, IPyAMSLayer, IView),
                provides=IViewContextPermissionChecker)
def form_handler_permission_checker(context, request, view):
    """Form handler permission checker"""
    registry = get_pyramid_registry()
    parent = get_parent(context, IFormHandlersTarget)
    return registry.queryMultiAdapter((parent, request, view),
                                      IViewContextPermissionChecker)

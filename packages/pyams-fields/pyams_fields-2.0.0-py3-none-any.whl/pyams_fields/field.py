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

"""PyAMS_fields.field module

This module defines standard fields types.
"""

from collections import OrderedDict

from persistent import Persistent
from zope.componentvocabulary.vocabulary import UtilityTerm, UtilityVocabulary
from zope.container.contained import Contained
from zope.schema import Bool, Choice, Date, Datetime, Int, List, Text, TextLine, Time, URI
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from pyams_fields.interfaces import IFormField, IFormFieldContainerTarget, PYAMS_FIELDS_TYPES, \
    IFormFieldFactory
from pyams_i18n.interfaces import II18n
from pyams_security.interfaces import IViewContextPermissionChecker
from pyams_utils.adapter import adapter_config
from pyams_utils.factory import factory_config
from pyams_utils.registry import get_pyramid_registry, utility_config
from pyams_utils.request import check_request
from pyams_utils.schema import DatesRangeField, DatetimesRangeField, DottedDecimalField, MailAddressField, TimezoneField
from pyams_utils.traversing import get_parent
from pyams_utils.vocabulary import vocabulary_config

__docformat__ = 'restructuredtext'

from pyams_fields import _


@factory_config(IFormField)
class FormField(Persistent, Contained):
    """Form field definition persistent class"""

    name = FieldProperty(IFormField['name'])
    field_type = FieldProperty(IFormField['field_type'])
    label = FieldProperty(IFormField['label'])
    description = FieldProperty(IFormField['description'])
    placeholder = FieldProperty(IFormField['placeholder'])
    values = FieldProperty(IFormField['values'])
    default = FieldProperty(IFormField['default'])
    required = FieldProperty(IFormField['required'])
    visible = FieldProperty(IFormField['visible'])

    def get_field_factory(self):
        """Field factory getter"""
        registry = get_pyramid_registry()
        return registry.queryUtility(IFormFieldFactory, name=self.field_type)


@adapter_config(required=IFormField,
                provides=IViewContextPermissionChecker)
def form_field_permission_checker(context):
    """Form field permission checker"""
    parent = get_parent(context, IFormFieldContainerTarget)
    return IViewContextPermissionChecker(parent)


#
# Form fields factories
#

@vocabulary_config(name=PYAMS_FIELDS_TYPES)
class FormFieldTypesVocabulary(UtilityVocabulary):
    """Form field types vocabulary"""

    interface = IFormFieldFactory

    def __init__(self, context, **kw):  # pylint: disable=super-init-not-called
        request = check_request()
        registry = request.registry
        translate = request.localizer.translate
        utils = [
            (name, translate(util.label))
            for (name, util) in sorted(registry.getUtilitiesFor(self.interface),
                                       key=lambda x: x[1].weight)
        ]
        self._terms = OrderedDict(
            (title, UtilityTerm(name, title))
            for name, title in utils
        )

    def __iter__(self):
        return iter(self._terms.values())


class BaseFormFieldFactory:
    """Base form field factory"""

    label = None
    field_factory = None
    weight = 0

    icon_class = ''

    def get_schema_field(self, field):
        """Schema field getter"""
        i18n = II18n(field)
        result = self.field_factory(title=i18n.query_attribute('label'),
                                    description=i18n.query_attribute('description'),
                                    required=field.required,
                                    default=i18n.query_attribute('default'))
        result.__name__ = field.name
        return result


@utility_config(name='textline',
                provides=IFormFieldFactory)
class TextLineFieldFactory(BaseFormFieldFactory):
    """Text line field factory"""

    label = _("Text")
    field_factory = TextLine
    weight = 10

    icon_class = 'fas fa-font'


@utility_config(name='text',
                provides=IFormFieldFactory)
class TextFieldFactory(BaseFormFieldFactory):
    """Text field factory"""

    label = _("Multi-lines text")
    field_factory = Text
    weight = 11

    icon_class = 'fas fa-comment'


@utility_config(name='bool',
                provides=IFormFieldFactory)
class BooleanFieldFactory(BaseFormFieldFactory):
    """Boolean field factory"""

    label = _("Boolean")
    field_factory = Bool
    weight = 20

    icon_class = 'far fa-square-check'


@utility_config(name='integer',
                provides=IFormFieldFactory)
class IntegerFieldFactory(BaseFormFieldFactory):
    """Integer field factory"""

    label = _("Integer")
    field_factory = Int
    weight = 30

    icon_class = 'fas fa-9'


@utility_config(name='decimal',
                provides=IFormFieldFactory)
class DecimalFieldFactory(BaseFormFieldFactory):
    """Decimal field factory"""

    label = _("Decimal")
    field_factory = DottedDecimalField
    weight = 40

    icon_class = 'fas fa-dollar-sign'


@utility_config(name='date',
                provides=IFormFieldFactory)
class DateFieldFactory(BaseFormFieldFactory):
    """Date field factory"""

    label = _("Date")
    field_factory = Date
    weight = 50

    icon_class = 'fas fa-calendar-day'


@utility_config(name='time',
                provides=IFormFieldFactory)
class TimeFieldFactory(BaseFormFieldFactory):
    """Time field factory"""

    label = _("Time")
    field_factory = Time
    weight = 52

    icon_class = 'fas fa-clock'


@utility_config(name='datetime',
                provides=IFormFieldFactory)
class DatetimeFieldFactory(BaseFormFieldFactory):
    """Datetime field factory"""

    label = _("Datetime")
    field_factory = Datetime
    weight = 54

    icon_class = 'fas fa-clock'


@utility_config(name='dates-range',
                provides=IFormFieldFactory)
class DatesRangeFieldFactory(BaseFormFieldFactory):
    """Dates range factory"""

    label = _("Dates range")
    field_factory = DatesRangeField
    weight = 56

    icon_class = 'fas fa-calendar-week'

    def get_schema_field(self, field):
        """Schema field getter"""
        i18n = II18n(field)
        result = self.field_factory(title=i18n.query_attribute('label'),
                                    description=i18n.query_attribute('description'),
                                    required=field.required,
                                    from_label=_("first date"),
                                    to_label=_("last date"))
        result.__name__ = field.name
        return result


@utility_config(name='datetime-range',
                provides=IFormFieldFactory)
class DatetimeRangeFieldFactory(BaseFormFieldFactory):
    """Datetime range factory"""

    label = _("Datetime range")
    field_factory = DatetimesRangeField
    weight = 58

    icon_class = 'fas fa-calendar-week'

    def get_schema_field(self, field):
        """Schema field getter"""
        i18n = II18n(field)
        result = self.field_factory(title=i18n.query_attribute('label'),
                                    description=i18n.query_attribute('description'),
                                    required=field.required,
                                    from_label=_("first date"),
                                    to_label=_("last date"))
        result.__name__ = field.name
        return result


@utility_config(name='phone_number',
                provides=IFormFieldFactory)
class PhoneNumberFieldFactory(BaseFormFieldFactory):
    """Phone number field factory"""

    label = _("Phone number")
    field_factory = TextLine
    weight = 60

    icon_class = 'fas fa-mobile-screen'


@utility_config(name='mail',
                provides=IFormFieldFactory)
class MailFieldFactory(BaseFormFieldFactory):
    """Mail field factory"""

    label = _("E-mail address")
    field_factory = MailAddressField
    weight = 70

    icon_class = 'fas fa-at'


@utility_config(name='uri',
                provides=IFormFieldFactory)
class URIFieldFactory(BaseFormFieldFactory):
    """URI field factory"""

    label = _("URI")
    field_factory = URI
    weight = 80

    icon_class = 'fas fa-globe'


class ValuesFieldFactory(BaseFormFieldFactory):
    """Values-based field factory"""


@utility_config(name='choice',
                provides=IFormFieldFactory)
class ChoiceFieldFactory(ValuesFieldFactory):
    """Choice field factory"""

    label = _("Choice")
    field_factory = Choice
    weight = 90

    icon_class = 'fas fa-list'

    def get_schema_field(self, field):
        i18n = II18n(field)
        vocabulary = SimpleVocabulary([
            SimpleTerm(v, title=v)
            for v in field.values
        ])
        result = self.field_factory(title=i18n.query_attribute('label'),
                                    description=i18n.query_attribute('description'),
                                    required=field.required,
                                    default=i18n.query_attribute('default'),
                                    vocabulary=vocabulary)
        result.__name__ = field.name
        return result


@utility_config(name='list',
                provides=IFormFieldFactory)
class ListFieldFactory(ValuesFieldFactory):
    """List field factory"""

    label = _("List")
    field_factory = List
    weight = 100

    icon_class = 'fas fa-table-list'

    def get_schema_field(self, field):
        i18n = II18n(field)
        vocabulary = SimpleVocabulary([
            SimpleTerm(v, title=v)
            for v in field.values
        ])
        result = self.field_factory(title=i18n.query_attribute('label'),
                                    description=i18n.query_attribute('description'),
                                    required=field.required,
                                    default=[i18n.query_attribute('default')],
                                    value_type=Choice(vocabulary=vocabulary))
        result.__name__ = field.name
        return result


@utility_config(name='timezone',
                provides=IFormFieldFactory)
class TimezoneFieldFactory(BaseFormFieldFactory):
    """Timezone field factory"""

    label = _("Timezone")
    field_factory = TimezoneField
    weight = 110

    icon_class = 'fas fa-globe'

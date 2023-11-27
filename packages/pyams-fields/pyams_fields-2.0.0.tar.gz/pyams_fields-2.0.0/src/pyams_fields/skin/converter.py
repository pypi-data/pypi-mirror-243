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

"""PyAMS_fields.skin.converter module

This module provides adapters which are used to convert form input
data in a human-readable string format.
"""

from zope.schema.interfaces import IBool, IDate, IDatetime, IDecimal, IList, ITime

from pyams_fields.interfaces import IFormFieldDataConverter
from pyams_layer.interfaces import IPyAMSUserLayer
from pyams_utils.adapter import ContextRequestAdapter, adapter_config
from pyams_utils.date import EXT_DATETIME_FORMAT, EXT_DATE_FORMAT, EXT_TIME_FORMAT, format_date, format_datetime
from pyams_utils.interfaces import MISSING_INFO
from pyams_utils.schema import IDatesRangeField, IDatetimesRangeField


__docformat__ = 'restructuredtext'

from pyams_fields import _


@adapter_config(required=(IBool, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class BooleanFieldDataConverter(ContextRequestAdapter):
    """Boolean field user data converter"""

    def convert(self, value):
        """Data converter"""
        translate = self.request.localizer.translate
        text = translate(_("yes")) if value else translate(_("no"))
        return f'{self.context.title}: {text}'


@adapter_config(required=(IDate, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class DateFieldDataConverter(ContextRequestAdapter):
    """Date field user data converter"""

    @staticmethod
    def convert(value):
        """Date value converter"""
        return format_date(value, EXT_DATE_FORMAT) if value else MISSING_INFO


@adapter_config(required=(ITime, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class TimeFieldDataConverter(ContextRequestAdapter):
    """Time field user data converter"""

    @staticmethod
    def convert(value):
        """Date value converter"""
        return value.strftime(EXT_TIME_FORMAT) if value else MISSING_INFO


@adapter_config(required=(IDatetime, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class DatetimeFieldDataConverter(ContextRequestAdapter):
    """Datetime field data converter"""

    @staticmethod
    def convert(value):
        """Datetime value converter"""
        return format_datetime(value, EXT_DATETIME_FORMAT) if value else MISSING_INFO


DATES_RANGE_START_FORMAT = _("from %d/%m/%Y")
DATES_RANGE_END_FORMAT = _("to %d/%m/%Y")


@adapter_config(required=(IDatesRangeField, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class DatesRangeFieldDataConverter(ContextRequestAdapter):
    """Dates range field data converter"""

    def convert(self, value):
        """Dates range value converter"""
        if not value:
            return MISSING_INFO
        from_date, to_date = value
        return f"{format_date(from_date, DATES_RANGE_START_FORMAT, self.request) if from_date else ''} " \
               f"{format_date(to_date, DATES_RANGE_END_FORMAT, self.request) if to_date else ''}"


DATETIMES_RANGE_START_FORMAT = _("from %d/%m/%Y at %H:%M")
DATETIMES_RANGE_END_FORMAT = _("to %d/%m/%Y at %H:%M")


@adapter_config(required=(IDatetimesRangeField, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class DatetimesRangeFieldDataConverter(ContextRequestAdapter):
    """Datetimes range field data converter"""

    def convert(self, value):
        """Datetimes range value converter"""
        if not value:
            return MISSING_INFO
        from_date, to_date = value
        return f"{format_date(from_date, DATETIMES_RANGE_START_FORMAT, self.request) if from_date else ''} " \
               f"{format_date(to_date, DATETIMES_RANGE_END_FORMAT, self.request) if to_date else ''}"


@adapter_config(required=(IDecimal, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class DecimalFieldDataConverter(ContextRequestAdapter):
    """Decimal field user data converter"""

    @staticmethod
    def convert(value):
        """Decimal value converter"""
        return str(value) if value else MISSING_INFO


@adapter_config(required=(IList, IPyAMSUserLayer),
                provides=IFormFieldDataConverter)
class ListFieldDataConverter(ContextRequestAdapter):
    """List field user data converter"""

    @staticmethod
    def convert(value):
        """List value converter"""
        return ', '.join(value) if value else MISSING_INFO

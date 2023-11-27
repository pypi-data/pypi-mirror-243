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

"""PyAMS_fields.skin module

This module provides base fields form rendering support.
"""

import datetime

import requests
from pyramid.csrf import get_csrf_token
from zope.interface import Invalid, alsoProvides
from zope.schema import Bool, TextLine

from pyams_fields.interfaces import ICaptchaInfo, ICaptchaManagerInfo, ICaptchaManagerTarget, IFormFieldContainer, \
    IFormFieldContainerTarget, IFormFieldDataConverter, IFormHandlersInfo, IRGPDInfo
from pyams_fields.skin.interfaces import IFormFieldContainerInputForm
from pyams_fields.skin.rgpd import RGPDConsentFieldWidget
from pyams_form.button import button_and_handler
from pyams_form.field import Fields
from pyams_form.form import AddForm
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.error import IErrorViewSnippet
from pyams_form.interfaces.form import IFormFields
from pyams_i18n.interfaces import II18n
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_portal.skin.page import PortalContextIndexPage
from pyams_skin.interfaces.widget import ISubmitWidget
from pyams_skin.schema.button import SubmitButton
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.text import text_to_html
from pyams_utils.timezone import tztime
from pyams_utils.traversing import get_parent
from pyams_utils.url import relative_url
from pyams_viewlet.viewlet import RawContentProvider


__docformat__ = 'restructuredtext'

from pyams_fields import _


CSRF_FIELD_NAME = 'csrf_token'
RECAPTCHA_FIELD_NAME = 'g-recaptcha-response'
RECAPTCHA_SETTING_NAME = 'pyams_fields.recaptcha.verify_url'
RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
RGPD_CONSENT_FIELD_NAME = 'rgpd_consent'

FORM_SUBMIT_ERROR = _("Can't submit form.")
MISSING_TOKEN_ERROR = _("Missing recaptcha token!")
INVALID_TOKEN_ERROR = _("Can't verify recaptcha token! Are you a robot?")


@adapter_config(required=(IFormFieldContainerTarget, IPyAMSLayer),
                provides=IFormFieldContainerInputForm)
class FormFieldContainerInputForm(AddForm):
    """Form fields container input form"""

    form_errors_message = FORM_SUBMIT_ERROR

    def get_ajax_handler(self):
        """Form action getter"""
        return relative_url(self.context, self.request, view_name='submit.html')

    def add_error(self, error, widget, status=None):
        """Add error to current list of form's errors"""
        if isinstance(error, str):
            error = Invalid(error)
        if isinstance(widget, str):
            widget = self.widgets[widget]
        snippet = self.request.registry.getMultiAdapter((error, self.request, widget, widget.field, self, self.context),
                                                        IErrorViewSnippet)
        snippet.update()
        widget.error = snippet
        self.widgets.errors += (snippet,)
        translate = self.request.localizer.translate
        if not self.status:
            self.status = translate(status or self.form_errors_message)
        self.status += f'\n{translate(error.args[0])}'

    def update_widgets(self, prefix=None):
        """Widgets update"""
        super().update_widgets(prefix)
        request = self.request
        for widget in self.widgets.values():
            if widget.field.__name__ == CSRF_FIELD_NAME:
                widget.name = CSRF_FIELD_NAME
                widget.mode = HIDDEN_MODE
                widget.value = get_csrf_token(request)
            elif widget.field.__name__ == RECAPTCHA_FIELD_NAME:
                widget.name = RECAPTCHA_FIELD_NAME
                widget.mode = HIDDEN_MODE
            elif widget.field.__name__ == RGPD_CONSENT_FIELD_NAME:
                widget.name = RGPD_CONSENT_FIELD_NAME
                widget.description = ' '
                widget.required = True
                rgpd_info = IRGPDInfo(self.context)
                user_rights = II18n(rgpd_info).query_attribute('rgpd_user_rights', request=request)
                if user_rights:
                    widget.suffix = RawContentProvider(html=f"<div><br />{text_to_html(user_rights, 'oid_to_href')}"
                                                            f"</div>")
                widget.object_data = {
                    'ams-validate-messages': {
                        'required': request.localizer.translate(
                            _("You can't submit this form without accepting data usage rules."))
                    }
                }
                alsoProvides(widget, IObjectData)
            else:
                field = IFormFieldContainer(self.context).get(widget.field.__name__)
                if field is not None:
                    # switch label and description for boolean fields
                    if field.field_type == 'bool':
                        widget.label = II18n(field).query_attribute('label',
                                                                    request=request)
                    elif field.field_type == 'choice':
                        if field.placeholder:
                            widget.prompt = True
                            widget.prompt_message = field.placeholder
                    else:
                        widget.placeholder = field.placeholder

    def get_oid(self):
        """Unique OID getter"""
        formatter = ''
        handlers_info = IFormHandlersInfo(self.context, None)
        if handlers_info is not None:
            formatter = handlers_info.submission_id_format or formatter
        now = tztime(datetime.datetime.utcnow())
        return now.strftime(formatter)

    @button_and_handler('Submit', name='submit', factory=SubmitButton)
    def submit_form(self, action):
        """Form submission"""
        request = self.request
        registry = request.registry
        data, errors = self.extract_data()
        if errors:
            self.status = request.localizer.translate(self.form_errors_message)
            return
        # remove custom data fields from handler data
        if CSRF_FIELD_NAME in data:
            del data[CSRF_FIELD_NAME]
        # check reCaptcha data
        captcha_info = ICaptchaInfo(self.context, None)
        if captcha_info is not None:
            captcha_settings = captcha_info.get_captcha_settings()
            if captcha_settings.get('use_captcha'):
                if RECAPTCHA_FIELD_NAME not in data:
                    self.add_error(Invalid(MISSING_TOKEN_ERROR), RECAPTCHA_FIELD_NAME)
                    return
                target = get_parent(self.context, ICaptchaManagerTarget)
                captcha_manager = ICaptchaManagerInfo(target, None)
                if captcha_manager is not None:
                    proxy_url = captcha_manager.get_proxy_url(request)
                    proxies = {'https': proxy_url} if proxy_url else {}
                    recaptcha_verify_api = registry.settings.get(RECAPTCHA_SETTING_NAME)
                    if not recaptcha_verify_api:
                        recaptcha_verify_api = RECAPTCHA_VERIFY_URL
                    verify = requests.post(recaptcha_verify_api, {
                        'secret': captcha_settings.get('server_key'),
                        'response': data[RECAPTCHA_FIELD_NAME]
                    }, proxies=proxies).json()
                    if not verify['success']:
                        self.add_error(INVALID_TOKEN_ERROR, RECAPTCHA_FIELD_NAME)
                        return
                del data[RECAPTCHA_FIELD_NAME]
        # convert form data to user friendly data
        user_data = data.copy()
        for form_field in IFormFieldContainer(self.context).get_fields():
            converter = registry.queryMultiAdapter((form_field, request), IFormFieldDataConverter)
            if converter is not None:
                user_data[form_field.__name__] = converter.convert(data.get(form_field.__name__))
            if not user_data[form_field.__name__]:
                user_data[form_field.__name__] = '--'
        request.annotations['submit.reference'] = user_data['_reference'] = self.get_oid()
        # call form handlers
        form_output = {}
        handlers_info = IFormHandlersInfo(self.context, None)
        if handlers_info is not None:
            for handler_name in handlers_info.handlers or ():
                handler = handlers_info.query_handler(handler_name)
                if handler is not None:
                    output = handler.handle(self.context, data, user_data)
                    if output:
                        form_output[handler_name] = output
        request.annotations['form.output'] = form_output

    def update_actions(self):
        """Actions update"""
        super().update_actions()
        submit = self.actions.get('submit')
        if submit is not None:
            alsoProvides(submit, ISubmitWidget)
            handlers_info = IFormHandlersInfo(self.context, None)
            if handlers_info is not None:
                submit.title = II18n(handlers_info).query_attribute('submit_label',
                                                                    request=self.request)


@adapter_config(required=(IFormFieldContainerTarget, IPyAMSLayer, IFormFieldContainerInputForm),
                provides=IFormFields)
def form_field_container_input_form_fields(context, request, view):
    """Form fields container input form fields getter"""

    registry = request.registry
    rgpd_consent_fieldname = registry.settings.get('pyams_fields.rgpd-consent.fieldname') or RGPD_CONSENT_FIELD_NAME

    def get_fields():
        """Form fields getter"""
        container = IFormFieldContainer(context)
        token = TextLine(title=_("CSRF token"), required=True)
        token.__name__ = CSRF_FIELD_NAME
        yield token
        captcha_info = ICaptchaInfo(context, None)
        if captcha_info is not None:
            captcha_settings = captcha_info.get_captcha_settings()
            if captcha_settings.get('use_captcha'):
                captcha = TextLine(title=_("Captcha"), required=True)
                captcha.__name__ = RECAPTCHA_FIELD_NAME
                yield captcha
        yield from container.get_fields()
        rgpd_info = IRGPDInfo(context, None)
        if (rgpd_info is not None) and rgpd_info.rgpd_consent:
            consent = Bool(title=II18n(rgpd_info).query_attribute('rgpd_warning', request=request),
                           required=True,
                           default=False)
            consent.__name__ = rgpd_consent_fieldname
            yield consent

    fields = Fields(*tuple(get_fields()))
    if rgpd_consent_fieldname in fields:
        fields[rgpd_consent_fieldname].widget_factory = RGPDConsentFieldWidget
    return fields


@pagelet_config(name='submit.html',
                context=IFormFieldContainerTarget, layer=IPyAMSLayer)
class FormSubmitPage(PortalContextIndexPage):
    """Form submit page"""

    input_form = None

    def __init__(self, context, request):
        super().__init__(context, request)
        self.input_form = request.registry.getMultiAdapter((context, self.request),
                                                           IFormFieldContainerInputForm)

    def update(self):
        """Page update"""
        super().update()
        self.input_form.update()

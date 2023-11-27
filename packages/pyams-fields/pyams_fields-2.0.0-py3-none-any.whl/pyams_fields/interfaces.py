#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_fields.interfaces module

"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.interface import Attribute, Interface
from zope.location.interfaces import IContained
from zope.schema import Bool, Choice, Int, List, TextLine

from pyams_i18n.schema import I18nHTMLField, I18nTextField, I18nTextLineField
from pyams_utils.schema import EncodedPasswordField, TextLineListField

from pyams_fields import _


PYAMS_FIELDS_TYPES = 'pyams_fields.types'

PYAMS_FIELDS_CONTAINER_KEY = 'pyams_fields.container'


class IFormField(IContained, IAttributeAnnotatable):
    """Form field interface"""

    containers('.IFormFieldContainer')

    name = TextLine(title=_("Field name"),
                    description=_("Field internal name; must be unique for a given form"),
                    required=True)

    field_type = Choice(title=_("Field type"),
                        description=_("Selected field type"),
                        vocabulary=PYAMS_FIELDS_TYPES,
                        required=True)

    label = I18nTextLineField(title=_("Label"),
                              description=_("User field label"),
                              required=True)

    description = I18nTextField(title=_("Description"),
                                description=_("Field description can be displayed as hint"),
                                required=False)

    placeholder = TextLine(title=_("Placeholder"),
                           description=_("Some field types like text line can display a "
                                         "placeholder"),
                           required=False)

    values = TextLineListField(title=_("Optional values"),
                               description=_("List of available values (for 'choice' and 'list' "
                                             "field types)"),
                               required=False)

    default = I18nTextLineField(title=_("Default value"),
                                description=_("Give default value if field type can use it"),
                                required=False)

    required = Bool(title=_("Required?"),
                    description=_("Select 'yes' to set field as mandatory"),
                    required=True,
                    default=False)

    visible = Bool(title=_("Visible?"),
                   description=_("Select 'no' to hide given field..."),
                   required=True,
                   default=True)


class IFormFieldFactory(Interface):
    """Form field factory interface"""

    label = Attribute("Factory label")
    weight = Attribute("Factory weight")

    def get_schema_field(self, field):
        """Get schema field matching given form field"""


class IFormFieldDataConverter(Interface):
    """Interface of a converter adapter which can be used to convert form data"""

    def convert(self, value):
        """Convert given input value to string"""


class IFormFieldContainer(IContainer):
    """Form fields container interface"""

    contains(IFormField)

    def append(self, field):
        """Append given field to container"""

    def get_fields(self):
        """Get schema fields matching current fields"""

    def find_fields(self, factory):
        """Find fields matching given factory (defined by its utility name)"""


class IFormFieldContainerTarget(IAttributeAnnotatable):
    """Form fields container target marker interface"""


CAPTCHA_MANAGER_INFO_KEY = 'pyams_fields.captcha'


class ICaptchaManagerInfo(Interface):
    """Form manager captcha info"""

    use_captcha = Bool(title=_("Use captcha"),
                       description=_("Use captcha to check form submission"),
                       required=True,
                       default=False)

    default_captcha_client_key = TextLine(title=_("Default client key"),
                                          description=_("This key is included into HTML code "
                                                        "and submitted with form data"),
                                          required=False)

    default_captcha_server_key = TextLine(title=_("Default server key"),
                                          description=_("This key is used on server side to "
                                                        "communicate with Google reCaptcha "
                                                        "services"),
                                          required=False)

    def get_captcha_settings(self):
        """Get default captcha settings"""

    use_proxy = Bool(title=_("Use proxy server?"),
                     description=_("If a proxy server is required to access recaptcha services, "
                                   "please set them here"),
                     required=True,
                     default=False)

    proxy_proto = Choice(title=_("Protocol"),
                         description=_("If your server is behind a proxy, please set it's "
                                       "protocol here; HTTPS support is required for reCaptcha"),
                         required=False,
                         values=('http', 'https'),
                         default='http')

    proxy_host = TextLine(title=_("Host name"),
                          description=_("If your server is behind a proxy, please set it's "
                                        "address here; captcha verification requires HTTPS "
                                        "support"),
                          required=False)

    proxy_port = Int(title=_("Port number"),
                     description=_("If your server is behind a proxy, please set it's port "
                                   "number here"),
                     required=False,
                     default=8080)

    proxy_username = TextLine(title=_("Username"),
                              description=_("If your proxy server requires authentication, "
                                            "please set username here"),
                              required=False)

    proxy_password = EncodedPasswordField(title=_("Password"),
                                          description=_("If your proxy server requires "
                                                        "authentication, please set password "
                                                        "here"),
                                          required=False)

    proxy_only_from = TextLine(title=_("Use proxy only from"),
                               description=_("If proxy usage is restricted to several domains "
                                             "names, you can set them here, separated by comas"),
                               required=False)

    def get_proxy_url(self, request):
        """Get proxy server URL"""


class ICaptchaManagerTarget(IAttributeAnnotatable):
    """Captcha manager target interface"""


class ICaptchaInfo(Interface):
    """Custom form captcha info interface"""

    override_captcha = Bool(title=_("Override default captcha settings"),
                            description=_("Select this option to define custom captcha keys "
                                          "for this form"),
                            required=True,
                            default=False)

    captcha_client_key = TextLine(title=_("Client key"),
                                  description=_("This key (also called 'site key') is included "
                                                "into HTML code and submitted with form data"),
                                  required=False)

    captcha_server_key = TextLine(title=_("Server key"),
                                  description=_("This key (also called 'secret key') is used on "
                                                "server side to communicate with Google "
                                                "reCaptcha services"),
                                  required=False)

    def get_captcha_settings(self):
        """Captcha settings getter

        Returns a dictionary containing client and server keys.
        """


class ICaptchaTarget(IAttributeAnnotatable):
    """Captcha target interface"""


RGPD_INFO_KEY = 'pyams_fields.rgpd'


class IRGPDInfo(Interface):
    """RGPD info interface"""

    rgpd_consent = Bool(title=_("Required RGPD consent"),
                        description=_("If 'yes', an RGPD compliance warning will be displayed "
                                      "above form's submit button; form can't be submitted as "
                                      "long as the associated checkbox will not be checked "
                                      "explicitly by the user"),
                        required=True,
                        default=False)

    rgpd_warning = I18nTextField(title=_("RGPD consent text"),
                                 description=_("User consent must be explicit, and user must be "
                                               "warned about usage which will be made of "
                                               "submitted data; text samples are given below"),
                                 required=False)

    rgpd_user_rights = I18nHTMLField(title=_("RGPD user rights"),
                                     description=_("The internet user must be able to easily "
                                                   "revoke his consent later on, so it is "
                                                   "important to inform him how to proceed; "
                                                   "below are examples of possible formulations"),
                                     required=False)


class IRGPDTarget(Interface):
    """RGPD info marker interface"""


#
# Forms handlers interfaces
#

class IFormHandler(Interface):
    """Form submission handler"""

    label = Attribute("Handler label")
    target_interface = Attribute("Handler target marker interface")

    def handle(self, form, data, user_data):
        """Handle entered data

        :param form: input form
        :param data: raw form data
        :param user_data: user friendly form input data
        """


class IFormHandlerInfo(Interface):
    """Form handler information base interface"""


FORM_HANDLERS_INFO_KEY = 'pyams_fields.handlers'
FORM_HANDLERS_VOCABULARY = 'pyams_fields.handlers'


class IFormHandlersInfo(IAttributeAnnotatable):
    """Form handlers settings interface

    This interface defines the list of handlers supported by a given
    form handler target context. Each selected handler will define how data
    submitted in a form will be taken in charge.
    """

    auth_only = Bool(title=_("Authenticated only?"),
                     description=_("If 'yes', only authenticated users will be able to see and "
                                   "submit form"),
                     required=False,
                     default=False)

    submit_label = I18nTextLineField(title=_("Submit button label"),
                                     description=_("Label of form submit button"),
                                     required=True)

    submit_message = I18nHTMLField(title=_("Submit message"),
                                   description=_("This message will be displayed after form "
                                                 "submission; you can include the submission ID using the "
                                                 "{_reference} syntax"),
                                   required=True)

    submission_id_format = TextLine(title=_("Submission ID format"),
                                    description=_("Submission ID is based on the current date and time, formatted "
                                                  "using this formatting string"),
                                    required=True,
                                    default='PyAMS-%Y%m%d-%H%M-%f')

    handlers = List(title=_("Selected handlers"),
                    description=_("The selected form handlers defines how user submitted data "
                                  "will be managed"),
                    value_type=Choice(vocabulary=FORM_HANDLERS_VOCABULARY),
                    required=False)

    def query_handler(self, name=None):
        """Query form handler matching given name"""


class IFormHandlersTarget(IAttributeAnnotatable):
    """Form handlers target marker interface"""

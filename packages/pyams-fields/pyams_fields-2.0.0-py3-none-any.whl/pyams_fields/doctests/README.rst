====================
PyAMS fields package
====================

Introduction
------------

This package is composed of a set of components usable into any Pyramid application.
It relies on the PyAMS framework and can't be used without it.

The goal of this package is to allow a content manager to be able to define a set of
custom schema fields, which can be used to generate users forms automatically.

For example, the PyAMS_content CMS package defines a *form* shared content, which can
be used to define any kind of form (contact form, registry form...). However, how the
submitted data will be processed is not handled by this package: you can define any set
of *handlers* in your own applications; the only default form handler which is provided
by PyAMS_content will send data using an email address.


Site upgrade
------------

PyAMS_fields relies on other packages which are needing a site upgrade:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)
    >>> from pyams_form import includeme as include_form
    >>> include_form(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_layer import includeme as include_layer
    >>> include_layer(config)
    >>> from pyams_viewlet import includeme as include_viewlet
    >>> include_viewlet(config)
    >>> from pyams_skin import includeme as include_skin
    >>> include_skin(config)
    >>> from pyams_fields import includeme as include_fields
    >>> include_fields(config)

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_site_before_traverse, get_local_registry
    >>> from pyams_site.generations import upgrade_site

    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...


Creating and using form fields
------------------------------

The first step is to create a container which will be able to receive form fields. This
container can be attached to a content implementing *IFormFieldsContainerTarget* interface:

    >>> from zope.interface import alsoProvides, implementer, Interface

    >>> from pyams_fields.interfaces import IFormFieldContainerTarget
    >>> alsoProvides(app, IFormFieldContainerTarget)

    >>> from pyams_fields.interfaces import IFormFieldContainer
    >>> container = IFormFieldContainer(app)
    >>> container
    <pyams_fields.container.FormFieldContainer object at 0x...>

Let's start by creating a first field:

    >>> from pyams_fields.field import FormField

    >>> field = FormField()
    >>> field.name = 'field1'
    >>> field.field_type = 'textline'
    >>> field.label = {'en': 'Field 1'}

    >>> field.get_field_factory()
    <pyams_fields.field.TextLineFieldFactory object at 0x...>

    >>> container[field.name] = field

    >>> list(container.keys())
    ['field1']
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>]

    >>> list(container.find_fields('textline'))
    [<pyams_fields.field.FormField object at 0x...>]

Form fields target provides traverser and sublocations to get access to fields container:

    >>> from zope.traversing.interfaces import ITraversable

    >>> traverser = request.registry.queryAdapter(app, ITraversable, name='fields')
    >>> traverser.traverse('') is container
    True
    >>> traverser.traverse('field1') is field
    True

    >>> from zope.location.interfaces import ISublocations
    >>> locations = request.registry.queryAdapter(app, ISublocations, name='fields')
    >>> list(locations.sublocations())
    [<pyams_fields.field.FormField object at 0x...>]


Form fields permission checker
------------------------------

Form fields container get their permission checker from their context:

    >>> from pyams_security.interfaces import IViewContextPermissionChecker

    >>> try:
    ...     checker = request.registry.queryAdapter(field, IViewContextPermissionChecker)
    ... except TypeError:
    ...     checker = None

    >>> checker is None
    True

This error is due to the fact that we actually don't have a permission checker on site root!
Let's create one:

    >>> from pyams_utils.adapter import ContextAdapter
    >>> from pyams_site.interfaces import ISiteRoot

    >>> class SiteRootAdapter(ContextAdapter):
    ...     edit_permission = 'edit'

    >>> request.registry.registerAdapter(SiteRootAdapter, (ISiteRoot,), IViewContextPermissionChecker)

    >>> checker = request.registry.queryAdapter(field, IViewContextPermissionChecker)
    >>> checker
    <pyams_fields.tests.test_utilsdocs.SiteRootAdapter object at 0x...>
    >>> checker.context is app
    True

    >>> checker.edit_permission
    'edit'


Custom form fields
------------------

Choice and List fields require a custom schema field factory and a set of selection values:

    >>> field2 = FormField()
    >>> field2.name = 'field2'
    >>> field2.field_type = 'choice'
    >>> field2.label = {'en': 'Field 2'}
    >>> field2.values = ["Value 1", "Value 2"]

    >>> container['field2'] = field2
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>, <zope.schema._field.Choice object at 0x... field2>]

    >>> field3 = FormField()
    >>> field3.name = 'field3'
    >>> field3.field_type = 'list'
    >>> field3.label = {'en': 'Field 3'}
    >>> field3.values = ["Value 1", "Value 2"]

    >>> field2.visible = False

    >>> container['field3'] = field3
    >>> list(container.get_fields())
    [<zope.schema._bootstrapfields.TextLine object at 0x... field1>, <zope.schema._field.List object at 0x... field3>]
    >>> list(container.find_fields('choice'))
    []


Form captcha settings
---------------------

PyAMS_fields allows usage of Google reCaptcha to validate forms. Captcha settings allow to define
client and server keys, as well as a proxy configuration which may be required to access Google
services:

    >>> from zope.interface import alsoProvides
    >>> from zope.container.folder import Folder
    >>> from pyams_fields.interfaces import ICaptchaManagerInfo, ICaptchaManagerTarget, ICaptchaInfo, ICaptchaTarget

    >>> alsoProvides(app, ICaptchaManagerTarget)

    >>> captcha_info = ICaptchaManagerInfo(app)
    >>> captcha_info
    <pyams_fields.captcha.CaptchaManagerInfo object at 0x...>

    >>> captcha_info.default_captcha_client_key = 'client_key'
    >>> captcha_info.default_captcha_server_key = 'server_key'
    >>> captcha_info.use_captcha = True

    >>> captcha_info.get_captcha_settings()
    {'use_captcha': True, 'client_key': 'client_key', 'server_key': 'server_key'}

    >>> captcha_info.get_proxy_url(request) is None
    True

    >>> captcha_info.proxy_proto = 'https'
    >>> captcha_info.proxy_host = 'proxy.example.com'
    >>> captcha_info.proxy_port = 8080
    >>> captcha_info.proxy_username = 'username'
    >>> captcha_info.proxy_password = 'password'
    >>> captcha_info.use_proxy = True

    >>> captcha_info.get_proxy_url(request)
    'https://username:password@proxy.example.com:8080/'

You can set domains for which proxy usage is required:

    >>> captcha_info.proxy_only_from = 'example.com'

    >>> captcha_info.get_proxy_url(request) is None
    True

    >>> request = DummyRequest(host='example.com')
    >>> captcha_info.get_proxy_url(request)
    'https://username:password@proxy.example.com:8080/'

Please note that these settings are *default* settings, which can be customized for a given
context:

    >>> alsoProvides(container, ICaptchaTarget)

    >>> app['container'] = container

    >>> fields_info = ICaptchaInfo(container)
    >>> fields_info
    <pyams_fields.captcha.CaptchaInfo object at 0x...>

    >>> fields_info.override_captcha
    False

    >>> fields_info.get_captcha_settings()
    {'use_captcha': True, 'client_key': 'client_key', 'server_key': 'server_key'}

    >>> fields_info.override_captcha = True

    >>> fields_info.get_captcha_settings()
    {'use_captcha': False, 'client_key': None, 'server_key': None}

    >>> fields_info.captcha_client_key = 'custom_client_key'
    >>> fields_info.captcha_server_key = 'custom_server_key'

    >>> fields_info.get_captcha_settings()
    {'use_captcha': True, 'client_key': 'custom_client_key', 'server_key': 'custom_server_key'}


Forms handlers
--------------

Form handlers are utilities which can handle submitted form data.

    >>> from pyams_utils.registry import utility_config
    >>> from pyams_utils.testing import call_decorator

    >>> from pyams_fields.interfaces import IFormHandler, IFormHandlersTarget, IFormHandlersInfo
    >>> alsoProvides(container, IFormHandlersTarget)

    >>> handlers_info = IFormHandlersInfo(container)
    >>> handlers_info
    <pyams_fields.handler.FormHandlersInfo object at 0x...>

Let's create a simple handler which will log submitted data:

    >>> class ISimpleFormHandler(IFormHandler):
    ...     """Simple form handler interface"""

    >>> class ISimpleFormHandlerTarget(Interface):
    ...     """Simple form handler target marker interface"""

    >>> @implementer(ISimpleFormHandler)
    ... class SimpleFormHandler:
    ...
    ...     label = "Simple handler"
    ...     target_interface = ISimpleFormHandlerTarget
    ...
    ...     def handle(self, form, data, user_data):
    ...         print(user_data)

    >>> call_decorator(config, utility_config, SimpleFormHandler, name='simple_handler', provides=IFormHandler)

    >>> handlers_info.handlers = ['simple_handler']
    >>> handlers_info.handlers
    ['simple_handler']
    >>> ISimpleFormHandlerTarget.providedBy(handlers_info)
    True

Specifying a missing handler is not allowed:

    >>> handlers_info.handlers = ['simple_handler', 'missing_handler']
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.WrongContainedType: ([ConstraintNotSatisfied('missing_handler', '')], 'handlers')

    >>> handlers_info.handlers = []
    >>> ISimpleFormHandlerTarget.providedBy(handlers_info)
    False

Form handlers can be traversed:

    >>> from pyams_fields.handler import FormHandlersTraverser
    >>> FormHandlersTraverser(container).traverse('') is handlers_info
    True

    >>> from pyams_fields.handler import FormHandlerInfoTraverser
    >>> FormHandlerInfoTraverser(container).traverse('simple_handler') is None
    True

This result is normal, because we should register an adapter from the form handler target
interface to *IFormHandlerInfo*, using the same name for form handler and for adapter. This adapter
can then be used, for example, to store additional information related to this form handler
configuration.


Tests cleanup:

    >>> tearDown()

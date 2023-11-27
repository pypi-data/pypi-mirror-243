===================
pyams_auth_azure package
===================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> import pprint

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> from pyramid.threadlocal import manager
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from beaker.cache import CacheManager, cache_regions
    >>> cache = CacheManager(**{'cache.type': 'memory'})
    >>> cache_regions.update({'default': {'type': 'memory', 'expire': 60}})

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_security import includeme as include_security
    >>> include_security(config)
    >>> from pyams_form import includeme as include_form
    >>> include_form(config)
    >>> from pyams_skin import includeme as include_skin
    >>> include_skin(config)
    >>> from pyams_zmi import includeme as include_zmi
    >>> include_zmi(config)
    >>> from pyams_auth_azure import includeme as include_auth_azure
    >>> include_auth_azure(config)

    >>> from pyams_utils.registry import get_utility, set_local_registry
    >>> registry = config.registry
    >>> set_local_registry(registry)

    >>> from pyams_site.generations import upgrade_site
    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS security to generation 2...

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyams_utils.registry import handle_site_before_traverse
    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))

    >>> from pyams_security.interfaces import ISecurityManager
    >>> sm = get_utility(ISecurityManager)

    >>> from pyams_security.interfaces.plugin import ICredentialsPlugin
    >>> plugin = get_utility(ICredentialsPlugin, name='azure')


Using Azure authentication
--------------------------

    >>> plugin in sm.credentials_plugins
    True
    >>> plugin in sm.authentication_plugins
    False
    >>> plugin in sm.directory_plugins
    False

You have to set several security manager properties to use JWT:

    >>> from pyams_utils.factory import register_factory
    >>> from pyams_auth_azure.interfaces import IAzureSecurityConfiguration
    >>> from pyams_auth_azure.plugin import AzureSecurityConfiguration
    >>> register_factory(IAzureSecurityConfiguration, AzureSecurityConfiguration)

    >>> azure_configuration = IAzureSecurityConfiguration(sm)
    >>> azure_configuration.test_header = 'X-Test'
    >>> azure_configuration.enabled = True

    >>> plugin.enabled
    True

    >>> request = DummyRequest(headers={'X-Test': 1, 'Authorization': 'Bearer admin'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials
    <pyams_security.credential.Credentials object at 0x...>
    >>> credentials.prefix
    'azure'
    >>> credentials.id
    'system:admin'
    >>> credentials.attributes.get('login')
    'admin'

We can try to start a new request to test caching:

    >>> request = DummyRequest(headers={'X-Test': 1, 'Authorization': 'Bearer admin'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials
    <pyams_security.credential.Credentials object at 0x...>

We can now try with bad requests. With a missing principal:

    >>> request = DummyRequest(headers={'X-Test': 1, 'Authorization': 'Bearer missing'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials is None
    True

With a bad authentication schema:

    >>> request = DummyRequest(headers={'X-Test': 1, 'Authorization': 'JWT admin'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials is None
    True

With a missing authorization header:

    >>> request = DummyRequest(headers={'X-Test': 1, 'X-BAD-Authorization': 'Bearer admin'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials is None
    True

With a disable plug-in:

    >>> azure_configuration.enabled = False
    >>> request = DummyRequest(headers={'X-Test': 1, 'Authorization': 'Bearer admin'})
    >>> credentials = plugin.extract_credentials(request)
    >>> credentials is None
    True


Testing configuration form
--------------------------

    >>> from zope.interface import alsoProvides
    >>> from pyams_layer.interfaces import IFormLayer

    >>> request = DummyRequest(context=sm)
    >>> alsoProvides(request, IFormLayer)

    >>> from pyams_auth_azure.zmi.plugin import AzureSecurityConfigurationEditForm

    >>> form = AzureSecurityConfigurationEditForm(sm, request)
    >>> form.update()
    >>> form.get_content() is azure_configuration
    True


Tests cleanup:

    >>> tearDown()

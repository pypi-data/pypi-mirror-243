#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_auth_azure.plugin module

This module provides main Azure authentication plug-in.
"""

import logging

from ZODB.POSException import ConnectionStateError
from msal import ConfidentialClientApplication
from persistent import Persistent
from zope.container.contained import Contained
from zope.schema.fieldproperty import FieldProperty

from pyams_auth_azure.interfaces import AZURE_CONFIGURATION_KEY, IAzureAuthenticationPlugin, \
    IAzureSecurityConfiguration
from pyams_security.credential import Credentials
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.plugin import ICredentialsPlugin
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.cache import get_cache
from pyams_utils.factory import factory_config
from pyams_utils.list import boolean_iter
from pyams_utils.property import ClassPropertyType, classproperty
from pyams_utils.registry import get_utility, query_utility, utility_config


__docformat__ = 'restructuredtext'

from pyams_auth_azure import _  # pylint: disable=ungrouped-imports

LOGGER = logging.getLogger('PyAMS (security)')


@factory_config(IAzureSecurityConfiguration)
class AzureSecurityConfiguration(Persistent, Contained):
    """Azure security configuration"""

    enabled = FieldProperty(IAzureSecurityConfiguration['enabled'])
    client_id = FieldProperty(IAzureSecurityConfiguration['client_id'])
    secret_key = FieldProperty(IAzureSecurityConfiguration['secret_key'])
    authority = FieldProperty(IAzureSecurityConfiguration['authority'])
    verify_ssl = FieldProperty(IAzureSecurityConfiguration['verify_ssl'])
    authorization_header = FieldProperty(IAzureSecurityConfiguration['authorization_header'])
    authorization_scheme = FieldProperty(IAzureSecurityConfiguration['authorization_scheme'])
    test_header = FieldProperty(IAzureSecurityConfiguration['test_header'])
    use_cache = FieldProperty(IAzureSecurityConfiguration['use_cache'])
    selected_cache = FieldProperty(IAzureSecurityConfiguration['selected_cache'])


@adapter_config(required=ISecurityManager, provides=IAzureSecurityConfiguration)
def security_manager_azure_configuration_factory(context):
    """Security manager Azure configuration factory adapter"""
    return get_annotation_adapter(context, AZURE_CONFIGURATION_KEY, IAzureSecurityConfiguration)


@utility_config(provides=IAzureAuthenticationPlugin)
@utility_config(name='azure', provides=ICredentialsPlugin)
class AzureAuthenticationPlugin(metaclass=ClassPropertyType):
    """Azure authentication plug-in"""

    prefix = 'azure'
    title = _("Azure authentication")

    @classproperty
    def configuration(cls):  # pylint: disable=no-self-argument,no-self-use
        """Azure configuration getter"""
        try:
            sm = query_utility(ISecurityManager)  # pylint: disable=invalid-name
            if sm is not None:
                return IAzureSecurityConfiguration(sm)
        except ConnectionStateError:
            return None
        return None

    @classproperty
    def enabled(cls):  # pylint: disable=no-self-argument,no-self-use
        """Check if Azure authentication is enabled in security manager"""
        configuration = cls.configuration
        try:
            return configuration.enabled if (configuration is not None) else False
        except ConnectionStateError:
            return False

    @staticmethod
    def find_principal(login):
        """Try to get principals for given login"""
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        found, principals = boolean_iter(sm.find_principals(login, exact_match=True))
        if not found:
            LOGGER.warning("Principal not found: %s", login)
            return None
        return next(principals)

    def extract_credentials(self, request, **kwargs):  # pylint: disable=unused-argument
        """Extract credentials from Azure token"""
        configuration = self.configuration
        if (configuration is None) or not configuration.enabled:
            return None
        authorization = request.headers.get(configuration.authorization_header)
        if not authorization:
            return None
        try:
            schema, token = authorization.split(' ', 1)
        except ValueError:
            return None
        if schema != configuration.authorization_scheme:
            return None
        LOGGER.debug("Got Azure token: %s", token)

        # Check Beaker cache
        cache = None
        if configuration.use_cache:
            cache = get_cache('azure_tokens', configuration.selected_cache,
                              'PyAMS-auth-azure::tokens')
            try:
                principal = cache.get_value(token)
            except KeyError:
                pass
            else:
                return Credentials(self.prefix,
                                   principal.get('principal_id'),
                                   login=principal.get('login'))

        # Use custom test mode header?
        login = None
        test_header = configuration.test_header
        if test_header and request.headers.get(test_header):
            login = token

        # Use MSAL to check token validity
        if not login:
            application = ConfidentialClientApplication(configuration.client_id,
                                                        authority=configuration.authority,
                                                        client_credential=configuration.secret_key,
                                                        verify=configuration.verify_ssl)
            auth_token = application.acquire_token_on_behalf_of(token, ['User.Read'])
            if 'access_token' not in auth_token:
                LOGGER.warning("Missing access token!")
                LOGGER.warning("Auth token: %s", str(auth_token))
            else:
                for account in application.get_accounts():
                    login = account.get('username')
                    if not login:
                        LOGGER.warning("Missing account user name!")
                        LOGGER.warning("Account data: %s", str(account))
                        continue
                    break

        # Find principal from login
        if login:
            principal = self.find_principal(login)
            if principal is not None:
                if cache is not None:
                    cache.set_value(token, {
                        'principal_id': principal.id,
                        'login': login
                    })
                return Credentials(self.prefix,
                                   principal.id,
                                   login=login)

        # empty fallback...
        return None

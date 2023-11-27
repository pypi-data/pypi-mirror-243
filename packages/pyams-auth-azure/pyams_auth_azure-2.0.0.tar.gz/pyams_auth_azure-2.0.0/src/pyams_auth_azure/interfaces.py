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

"""PyAMS_auth_azure.interfaces module

This module defines plug-in public interfaces.
"""

from zope.interface import Attribute, Interface, Invalid, invariant
from zope.schema import Bool, Choice, TextLine

from pyams_security.interfaces.plugin import ICredentialsPlugin
from pyams_utils.cache import BEAKER_CACHES_VOCABULARY

from pyams_auth_azure import _


AZURE_CONFIGURATION_KEY = 'pyams_auth_azure.configuration'
"""Main Azure configuration key"""


class IAzureSecurityConfiguration(Interface):
    """Security manager configuration interface for Azure authentication"""

    enabled = Bool(title=_("Enable Azure authentication?"),
                   description=_("Enable login via Azure authentication"),
                   required=False,
                   default=False)

    client_id = TextLine(title=_("Client ID"),
                         description=_("Application client ID"),
                         required=False)

    secret_key = TextLine(title=_("Secret key"),
                          description=_("Application secret key"),
                          required=False)

    authority = TextLine(title=_("Authentication authority"),
                         description=_("URL of the authentication authority"),
                         required=False)

    @invariant
    def check_configuration(self):
        """Check Azure configuration"""
        if self.enabled and not (self.client_id and self.secret_key and self.authority):
            raise Invalid(_("Client ID, secret key and authentication authority are required "
                            "to enable Azure authentication"))

    verify_ssl = Bool(title=_("Verify SSL?"),
                      description=_("If 'no', SSL certificates will not be verified"),
                      required=False,
                      default=True)

    authorization_header = TextLine(title=_("Authorization header"),
                                    description=_("Name of the HTTP header containing "
                                                  "authentication token"),
                                    required=True,
                                    default='Authorization')

    authorization_scheme = Choice(title=_("Authorization scheme"),
                                  description=_("Name of the prefix used in HTTP header"),
                                  values=('Bearer', 'JWT'),
                                  default='Bearer')

    test_header = TextLine(title=_("Test header"),
                           description=_("If this header is set and present into request "
                                         "headers (with any value), the authorization header "
                                         "value will be used \"as is\" without any Azure "
                                         "authentication to get user's login..."),
                           required=False)

    use_cache = Bool(title=_("Use authorization cache?"),
                     description=_("If selected, this option allows to store credentials in a "
                                   "local cache from which they can be reused"),
                     required=False,
                     default=True)

    selected_cache = Choice(title=_("Selected tokens cache"),
                            description=_("Beaker cache selected to store validated tokens"),
                            required=False,
                            vocabulary=BEAKER_CACHES_VOCABULARY,
                            default='default')


class IAzureAuthenticationPlugin(ICredentialsPlugin):
    """Azure authentication plugin interface"""

    configuration = Attribute("Azure configuration")
    enabled = Attribute("Enable Azure authentication?")

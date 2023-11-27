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

"""PyAMS_auth_azure.zmi.plugin module

This module defines views used to manage Azure plug-in configuration.
"""

from zope.interface import Interface

from pyams_auth_azure.interfaces import IAzureSecurityConfiguration
from pyams_form.ajax import ajax_form_config
from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.field import Fields
from pyams_form.interfaces.form import IGroup
from pyams_layer.interfaces import IPyAMSLayer
from pyams_security.interfaces import ISecurityManager
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security_views.zmi import ISecurityMenu
from pyams_skin.interfaces.viewlet import IHeaderViewletManager
from pyams_skin.viewlet.help import AlertMessage
from pyams_utils.adapter import adapter_config
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminEditForm, FormGroupChecker
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.zmi.viewlet.menu import NavigationMenuItem


__docformat__ = 'restructuredtext'

from pyams_auth_azure import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='azure-security-configuration.menu',
                context=ISecurityManager, layer=IAdminLayer,
                manager=ISecurityMenu, weight=70,
                permission=MANAGE_SECURITY_PERMISSION)
class AzureSecurityConfigurationMenu(NavigationMenuItem):
    """Azure security configuration menu"""

    label = _("Azure configuration")
    href = '#azure-security-configuration.html'


@ajax_form_config(name='azure-security-configuration.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class AzureSecurityConfigurationEditForm(AdminEditForm):
    """Azure security configuration edit form"""

    title = _("Security manager")
    legend = _("Azure configuration")

    fields = Fields(Interface)

    def get_content(self):
        return IAzureSecurityConfiguration(self.context)


@adapter_config(name='azure-configuration',
                required=(ISecurityManager, IAdminLayer, AzureSecurityConfigurationEditForm),
                provides=IGroup)
class AzureConfigurationGroup(FormGroupChecker):
    """Azure configuration edit group"""

    fields = Fields(IAzureSecurityConfiguration).omit('use_cache', 'selected_cache')
    fields['verify_ssl'].widget_factory = SingleCheckBoxFieldWidget


@viewlet_config(name='jwt-configuration.header',
                context=ISecurityManager, layer=IAdminLayer, view=AzureConfigurationGroup,
                manager=IHeaderViewletManager, weight=1)
class AzureConfigurationHeader(AlertMessage):
    """Azure configuration header"""

    status = 'info'

    _message = _("Azure authentication plug-in support the \"on-behalf-of\" flow, where a "
                 "resource declared on the Azure portal can be accessed, using an MSAL "
                 "client package, through an application proxy.\n"
                 "The original Azure authentication token received by the \"client\" is then "
                 "forwarded to the Pyramid application server, using another HTTP header; the "
                 "application can then use the Azure API to check token validity and extract "
                 "some of it's credentials (like a user ID) for which a lookup will be made "
                 "into another internal users directory...")


@adapter_config(name='azure-cache-configuration',
                required=(ISecurityManager, IAdminLayer, AzureConfigurationGroup),
                provides=IGroup)
class AzureCacheConfigurationGroup(FormGroupChecker):
    """Azure cache configuration edit group"""

    fields = Fields(IAzureSecurityConfiguration).select('use_cache', 'selected_cache')

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

"""PyAMS_chat.interfaces module

This module defines main chat interfaces.
"""

from zope.interface import Attribute, Interface
from zope.schema import Dict, Text, TextLine, URI

from pyams_chat import _


CHAT_PING_ROUTE = 'chat.ping'
CHAT_WORKER_ROUTE = 'chat.worker'

REST_CONTEXT_ROUTE = 'chat.rest.context'
REST_NOTIFICATIONS_ROUTE = 'chat.rest.notifications'


class IChatMessage(Interface):
    """Chat message interface"""

    host = TextLine(title=_("Message host name"))

    channel = TextLine(title=_("Message channel"))

    action = TextLine(title=_("Message action"))

    category = TextLine(title=_("Message category"))

    status = TextLine(title=_("Message status"))

    title = TextLine(title=_("Message title"))

    message = Text(title=_("Message content"))

    image = URI(title=_("Message image URL"),
                required=False)

    source = Dict(title=_("Message source"),
                  description=_("Attributes of the principal which emitted the notification"),
                  key_type=TextLine(),
                  value_type=TextLine())

    target = Dict(title=_("Message target"),
                  description=_("Message targets can be principals, roles..."),
                  key_type=TextLine())

    url = TextLine(title=_("Notification URL"),
                   description=_("URL target of this message notification"),
                   required=False)

    timestamp = TextLine(title=_("Message timestamp in ISO-8601 format"))

    user_data = Dict(title=_("Internal user data"),
                     description=_("User data used for internal usage; these data are not "
                                   "sent in notifications contents"))

    def send(self):
        """Send notification to recipients"""


class IChatMessageExtension(Interface):
    """Chat message extension interface

    These extensions, defined as adapters, can be used to add custom
    information to an existing message.

    This interface doesn't provide any method, as adapters should
    directly extend the original message.
    """

    weight = Attribute("Optional ordering weight")


class IChatMessageHandler(Interface):
    """Chat message handler interface

    This interface is used to define adapters which can be used to
    define a message target based on it's category.
    """

    weight = Attribute("Optional ordering weight")

    def get_target(self):
        """Get message target"""


class IRedisClient(Interface):
    """Redis client interface for chat"""

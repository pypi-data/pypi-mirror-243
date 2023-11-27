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

"""PyAMS_zmq.interfaces module

"""

from zope.interface import Attribute, Interface, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent


class IZMQProcess(Interface):
    """ZeroMQ process interface"""

    socket_type = Attribute("Socket type")

    def setup(self):
        """Initialize process context and events loop and initialize stream"""

    # pylint: disable=too-many-arguments
    def stream(self, sock_type, addr, bind, callback=None, subscribe=b''):
        """Create ZMQStream"""

    def init_stream(self):
        """initialize response stream"""

    def start(self):
        """Start the process"""

    def stop(self):
        """Stop the process"""


class IZMQProcessStartedEvent(IObjectEvent):
    """ZMQ process started event interface"""


@implementer(IZMQProcessStartedEvent)
class ZMQProcessStartedEvent(ObjectEvent):
    """ZMQ process started event"""


class IZMQMessageHandler(Interface):
    """ZeroMQ message handler"""

    handler = Attribute("Concrete message handler")

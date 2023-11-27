#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zmq.handler module

This module defines the base ZeroMQ message handler class.
"""

__docformat__ = 'restructuredtext'

from zmq.utils import jsonapi
from zope.interface import implementer

from pyams_zmq.interfaces import IZMQMessageHandler


@implementer(IZMQMessageHandler)
class ZMQMessageHandler:
    """Base class for message handlers for a :class:`pyams_zmq.process.Process`.

    Inheriting classes only need to implement a handler function for each
    message type.
    """

    handler = None

    def __init__(self, process, stream, stop, handler=None, json_load=-1):
        # pylint: disable=too-many-arguments
        # ZMQ parent process
        self.process = process
        self._json_load = json_load
        # Response stream
        self.rep_stream = stream
        self._stop = stop
        # Response handler
        self.rep_handler = handler or self.handler()  # pylint: disable=not-callable
        self.rep_handler.process = process

    def __call__(self, msg):
        """Gets called when a message is received by the stream this handler is
        registered with.

        :param msg: message content; it's a list as returned by
            :meth:`zmq.core.socket.Socket.recv_multipart`.
        """
        # Try to JSON-decode the index "self._json_load" of the message
        i = self._json_load
        msg_type, data = jsonapi.loads(msg[i])
        msg[i] = data

        # Get the actual message handler and call it
        if msg_type.startswith('_'):
            raise AttributeError('%s starts with an "_"' % msg_type)

        rep = getattr(self.rep_handler, msg_type)(*msg)
        self.rep_stream.send_json(rep)

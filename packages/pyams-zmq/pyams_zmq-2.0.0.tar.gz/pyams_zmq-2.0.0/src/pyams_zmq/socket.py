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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

import zmq


def zmq_socket(address, socket_type=zmq.REQ, linger=0, protocol='tcp', auth=None):
    # pylint: disable=no-member
    """Get ØMQ socket

    auth is given as unicode 'username:password' string and automatically converted to bytes.
    """
    context = zmq.Context()
    socket = context.socket(socket_type)
    socket.setsockopt(zmq.LINGER, linger)  # pylint: disable=no-member
    if auth:
        socket.plain_username, socket.plain_password = auth.encode().split(b':', 1)
    socket.connect('{0}://{1}'.format(protocol, address))
    return socket


def zmq_response(socket, flags=zmq.POLLIN, timeout=10):  # pylint: disable=no-member
    """Get response from given socket"""
    poller = zmq.Poller()
    poller.register(socket, flags)
    if poller.poll(timeout * 1000):
        return socket.recv_json()
    return [503, "Connection timeout"]

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

import multiprocessing
import signal
import sys

import zmq
from tornado import ioloop
from zmq.auth.thread import ThreadAuthenticator
from zmq.eventloop import zmqstream
from zope.interface import implementer

from pyams_utils.registry import get_pyramid_registry
from pyams_zmq.interfaces import IZMQProcess, ZMQProcessStartedEvent


@implementer(IZMQProcess)
class ZMQProcess(multiprocessing.Process):
    # pylint: disable=too-many-instance-attributes
    """
    This is the base for all processes and offers utility methods
    for setup and creating new streams.
    """

    socket_type = zmq.REP  # pylint: disable=no-member
    auth_thread = None

    def __init__(self, bind_addr, handler, auth=None, clients=None, registry=None):
        # pylint: disable=too-many-arguments
        super().__init__()

        self.context = None
        """The ØMQ :class:`~zmq.Context` instance."""

        self.loop = None
        """PyZMQ's event loop (:class:`~zmq.eventloop.ioloop.IOLoop`)."""

        self.bind_addr = bind_addr
        self.rep_stream = None
        self.handler = handler
        self.passwords = dict([auth.split(':', 1)]) if auth else None
        self.clients = clients.split() if clients else None

        self.registry = registry

    def run(self):
        """Sets up everything and starts the event loop on process startup"""
        signal.signal(signal.SIGTERM, self.exit)
        # Setup ZeroMQ IO loop
        try:
            self.setup()
        except zmq.error.ZMQError:
            self.exit()
        else:
            registry = get_pyramid_registry()
            registry.notify(ZMQProcessStartedEvent(self))  # pylint: disable=no-member
            self.loop.start()

    def setup(self):
        """Creates a :attr:`context` and an event :attr:`loop` for the process."""
        ctx = self.context = zmq.Context()
        auth = self.auth_thread = ThreadAuthenticator(ctx)
        auth.start()
        if self.clients:
            auth.allow(*self.clients)  # pylint: disable=not-an-iterable
        if self.passwords:
            auth.configure_plain(domain='*', passwords=self.passwords)
        self.loop = ioloop.IOLoop.current()
        self.rep_stream, _ = self.stream(self.socket_type, self.bind_addr, bind=True)
        self.init_stream()

    def init_stream(self):
        """Initialize response stream"""
        self.rep_stream.on_recv(self.handler(self, self.rep_stream, self.stop))

    def stop(self):
        """Stops the event loop."""
        if self.loop is not None:
            self.loop.stop()
            self.loop = None
        if self.auth_thread is not None:
            self.auth_thread.stop()

    def exit(self, num=None, frame=None):  # pylint: disable=unused-argument
        """Process exit"""
        self.stop()
        sys.exit()

    def stream(self, sock_type, addr, bind, callback=None, subscribe=b''):
        # pylint: disable=too-many-arguments
        """Creates a :class:`~zmq.eventloop.zmqstream.ZMQStream`.

        :param sock_type: The ØMQ socket type (e.g. ``zmq.REQ``)
        :param addr: Address to bind or connect to formatted as *host:port*,
            *(host, port)* or *host* (bind to random port).
            If *bind* is ``True``, *host* may be:

            - the wild-card ``*``, meaning all available interfaces,
            - the primary IPv4 address assigned to the interface, in its
            numeric representation or
            - the interface name as defined by the operating system.

            If *bind* is ``False``, *host* may be:

            - the DNS name of the peer or
            - the IPv4 address of the peer, in its numeric representation.

            If *addr* is just a host name without a port and *bind* is
            ``True``, the socket will be bound to a random port.
        :param bind: Binds to *addr* if ``True`` or tries to connect to it
            otherwise.
        :param callback: A callback for
            :meth:`~zmq.eventloop.zmqstream.ZMQStream.on_recv`, optional
        :param subscribe: Subscription pattern for *SUB* sockets, optional,
            defaults to ``b''``.
        :returns: A tuple containg the stream and the port number.
        """
        sock = self.context.socket(sock_type)

        # add server authenticator
        if self.passwords:
            sock.plain_server = True

        # addr may be 'host:port' or ('host', port)
        if isinstance(addr, str):
            addr = addr.split(':')
        host, port = addr if len(addr) == 2 else (addr[0], None)

        # Bind/connect the socket
        if bind:
            if port:
                sock.bind('tcp://%s:%s' % (host, port))
            else:
                port = sock.bind_to_random_port('tcp://%s' % host)
        else:
            sock.connect('tcp://%s:%s' % (host, port))

        # Add a default subscription for SUB sockets
        if sock_type == zmq.SUB:  # pylint: disable=no-member
            sock.setsockopt(zmq.SUBSCRIBE, subscribe)  # pylint: disable=no-member

        # Create the stream and add the callback
        stream = zmqstream.ZMQStream(sock, self.loop)
        if callback:
            stream.on_recv(callback)

        return stream, int(port)


def process_exit_func(process=None):
    """Process exit func is required to correctly end the child process"""
    if process is not None:
        if process.is_alive():
            process.terminate()
        process.join()

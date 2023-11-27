===========================
PyAMS ZeroMQ helper package
===========================

PyAMS 'ZMQ' package can be used to build wrapper around ØMQ (or ZeroMQ) library to exchange
messages following all ØMQ possible usages.

At least two components are required to build a ØMQ based application:

- a ØMQ server

- a ØMQ client

The way client and server communicate depends on used ØMQ protocol.

We will take example on the medias conversion utility provided by 'pyams_media' package, which
allows you to automatically convert medias files (videos...) asynchronously as soon as they are
uploaded. The conversion process is a background process so doesn't return any result.

WARNING: tests coverage results may be incomplete because of multiprocessing usage!

The conversion process is a simple ØMQ process:

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp(hook_zca=True)

    >>> from cornice import includeme as include_cornice
    >>> include_cornice(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_zmq import includeme as include_zmq
    >>> include_zmq(config)

    >>> from multiprocessing import Process
    >>> from pyams_zmq.process import ZMQProcess, process_exit_func

    >>> converter_address = '127.0.0.1:25556'

    >>> class MyConversionProcess(Process):
    ...     """Conversion manager process"""
    ...
    ...     def __init__(self, settings, group=None, target=None, name=None, *args, **kwargs):
    ...         Process.__init__(self, group, target, name, args, kwargs)
    ...         self.settings = settings
    ...
    ...     def run(self):
    ...         settings = self.settings
    ...         path  = settings['path']
    ...         format = settings['format']
    ...         # you can virtually do anything you want with these settings

To be sure to run asynchronously, this process is managed by a thread:

    >>> import time
    >>> from threading import Thread

    >>> class ConversionThread(Thread):
    ...     """Conversion thread"""
    ...
    ...     def __init__(self, process):
    ...         Thread.__init__(self)
    ...         self.process = process
    ...
    ...     def run(self):
    ...         self.process.start()
    ...         self.process.join()

The conversion handler is the simple class to which conversion is delegated:

    >>> class ConversionHandler:
    ...     """Conversion handler"""
    ...     def convert(self, data):
    ...         ConversionThread(MyConversionProcess(data)).start()
    ...         return [200, 'OK']

The message handler receives the message and handle it:

    >>> from pyams_zmq.handler import ZMQMessageHandler
    >>> class ConversionMessageHandler(ZMQMessageHandler):
    ...     handler = ConversionHandler

    >>> class ConversionProcess(ZMQProcess):
    ...     """Medias conversion process"""

The ØMQ process is generally started on application startup; following tests are commented
because tests are stucked when running in test mode:

    >>> import atexit
    >>> process = ConversionProcess(converter_address, ConversionMessageHandler)
    >>> process.start()
    >>> time.sleep(2)
    >>> if process.is_alive():
    ...     atexit.register(process_exit_func, process=process)
    <function process_exit_func at 0x...>

Once all these elements are in place, you just have to create a ØMQ client context, open a
connection and send a message.

Messages are lists of two objects; the first one is the type of the message, which should match
a method name of the message handler; the second object is the method arguments:

    >>> import zmq
    >>> from pyams_zmq.socket import zmq_socket, zmq_response

    >>> settings = {'path': '/this/is/my/path',
    ...             'format': 'JPEG'}
    >>> message = ['convert', settings]

    >>> try:
    ...     socket = zmq_socket(converter_address)
    ... except:
    ...     response = [500, 'Error']
    ... else:
    ...     socket.send_json(message)
    ...     response = zmq_response(socket)
    >>> response
    [200, 'OK']


Tests cleanup:

    >>> process.stop()
    >>> tearDown()

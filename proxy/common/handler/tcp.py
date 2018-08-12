#! -*- coding: utf-8 -*-


import socket
import tornado.web
import tornado.iostream
import tornado.tcpclient


from proxy.common.logger import Logger
from proxy.common.decorator import ignore_exception


logger = Logger.get_logger(__name__)


class TcpProxyRequestHandler(object):
    @tornado.web.asynchronous
    def connect(self):
        client_stream, proxy_stream = None, None

        def on_client_socket_close(data):
            if proxy_stream.closed():
                return
            proxy_stream.write(data)

        def on_client_streaming(data):
            proxy_stream.write(data)

        def on_proxy_socket_close(data):
            if client_stream.closed():
                return
            client_stream.write(data)

        def on_proxy_streaming(data):
            client_stream.write(data)

        def on_client_connect():
            self.clear()
            logger.debug('Create tunel to {0} success'.format(self.request.uri))
            client_stream.read_until_close(on_client_socket_close, on_client_streaming)
            proxy_stream.read_until_close(on_proxy_socket_close, on_proxy_streaming)
            client_stream.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        client_stream = self.request.connection.stream
        target_host, target_port = self.request.uri.split(':')
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        proxy_stream = tornado.iostream.IOStream(proxy_socket)
        proxy_stream.connect((target_host, int(target_port)), on_client_connect)

        client_stream.write = ignore_exception('client socket may by closed')(client_stream.write)
        proxy_stream.write = ignore_exception('proxy socket may by closed')(proxy_stream.write)

#! -*- coding: utf-8 -*-


import tornado.web


from proxy import settings
from proxy.common.logger import Logger
from proxy.common.handler.tcp import TcpProxyRequestHandler
from proxy.common.handler.http import HttpProxyRequestHandler


logger = Logger.get_logger(__name__)


class ProxyRequestHandler(HttpProxyRequestHandler, TcpProxyRequestHandler, tornado.web.RequestHandler):
    SUPPORTED_METHODS = ('CONNECT', 'GET', 'HEAD', 'POST', 'DELETE', 'PATCH', 'PUT', 'OPTIONS')

    def __init__(self, *args, **kwargs):
        super(ProxyRequestHandler, self).__init__(*args, **kwargs)

    def prepare(self):
        user_map = settings.LOGIN_USERS
        if not user_map:
            return super(ProxyRequestHandler, self).prepare()
        basic_auth = self.request.headers.get('Authorization', None)
        if basic_auth:
            auth_mode, auth_base64 = basic_auth.split(' ', 1)
            auth_user, auth_passwd = auth_base64.decode('base64').split(':', 1)
            print auth_user, auth_passwd
            if auth_user in user_map and user_map[auth_user] == auth_passwd:
                return super(ProxyRequestHandler, self).prepare()
        else:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="::Basic Auth::"')
        return super(ProxyRequestHandler, self).prepare()

    def on_finish(self):
        super(ProxyRequestHandler, self).on_finish()

    def on_connection_close(self):
        logger.info('{0} closed socket'.format(self.request.remote_ip))


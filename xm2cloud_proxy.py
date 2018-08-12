#! -*- coding: utf-8 -*-


import sys
import tornado.ioloop
import tornado.options
import tornado.httpserver


from proxy.common.logger import Logger
from proxy.database import get_proxy_dir
from proxy.core.application import ProxyApplication
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, get_proxy_dir())


logger = Logger.get_logger(__name__)


if __name__ == '__main__':
    tornado.options.define('host', default='0.0.0.0', help='Listen host', type=str)
    tornado.options.define('port', default=8000, help='Listen host', type=int)
    tornado.options.define('debug', default=False, help='Debug mode', type=bool)

    app = ProxyApplication()
    srv = tornado.httpserver.HTTPServer(app)
    srv.listen(tornado.options.options.port, tornado.options.options.host)

    tornado.ioloop.IOLoop.instance().start()

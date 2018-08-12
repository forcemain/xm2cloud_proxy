#! -*- coding: utf-8 -*-


import tornado.web


from proxy.common.handler import ProxyRequestHandler


class ProxyApplication(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        handlers = [
            (r'.*', ProxyRequestHandler)
        ]

        super(ProxyApplication, self).__init__(handlers=handlers)

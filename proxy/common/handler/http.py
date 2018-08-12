#! -*- coding: utf-8 -*-


import tornado.web
import tornado.gen
import tornado.httpclient


class HttpProxyRequestHandler(object):
    def http_render(self, *args, **kwargs):
        client = tornado.httpclient.HTTPClient()
        req = tornado.httpclient.HTTPRequest(*args, **kwargs)
        rsp = client.fetch(req)

        self.write(rsp.body)
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        self.clear()
        request = self.request
        kwargs = {
            'body': request.body,
            'connect_timeout': 60,
            'request_timeout': 300,
            'method': request.method,
            'follow_redirects': True,
            'headers': request.headers,
            'allow_nonstandard_methods': True
        }
        self.http_render(request.uri, **kwargs)

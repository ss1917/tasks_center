#!/usr/bin/env python
# -*-coding:utf-8-*-

from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    pass


class LivenessProbe(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("I'm OK")
#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2017/4/14 上午9:42
role   : Version Update
'''
from shortuuid import uuid
from tornado import httpserver, ioloop
from tornado import options as tnd_options
from tornado.options import options, define
from tornado.web import Application as tornado_app

define("addr", default='0.0.0.0', help="run on the given ip address", type=str)
define("port", default=8000, help="run on the given port", type=int)
define("progid", default=str(uuid()), help="tornado progress id", type=str)


class Application(tornado_app):
    """ 定制 Tornado Application 集成日志、sqlalchemy 等功能 """

    def __init__(self, handlers=None, default_host="",
                 transforms=None, **settings):
        tnd_options.parse_command_line()
        #Logger().init_logger(options.progid)
        super(Application, self).__init__(handlers, default_host,
                                          transforms, **settings)
        http_server = httpserver.HTTPServer(self)
        http_server.listen(options.port, address=options.addr)
        self.io_loop = ioloop.IOLoop.instance()

    def start_server(self):
        """
        启动 tornado 服务
        :return:
        """
        try:
            print('progressid: %(progid)s' % dict(progid=options.progid))
            print('server address: %(addr)s:%(port)d' % dict(addr=options.addr,
                                                                   port=options.port))
            print('web server start sucessfuled.')
            self.io_loop.start()
        except KeyboardInterrupt:
            self.io_loop.stop()
        except:
            import traceback
            Logger.error(traceback.format_exc())


if __name__ == '__main__':
    pass
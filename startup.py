#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : task center
'''

import fire
from tornado.options import define
from libs.program import MainProgram
from settings import settings as app_settings
from biz.tasks.program import Application as DealApp
from biz.tasks.applications import Application as AcceptApp

#define("port", default=8000, help="run on the given port", type=int)
define("service", default='control_api', help="start service flag", type=str)
class MyProgram(MainProgram):
    def __init__(self, service='control_api', progressid=''):
        self.__app = None
        settings = app_settings
        if service == 'accept_api':
            self.__app = AcceptApp(**settings)
        elif service == 'exec_task':
            self.__app = DealApp(**settings)
        super(MyProgram, self).__init__(progressid)
        self.__app.start_server()

if __name__ == '__main__':
    fire.Fire(MyProgram)
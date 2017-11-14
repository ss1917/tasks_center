#!/usr/bin/env python
# -*-coding:utf-8-*-

#from biz.tasks.handlers import task_control_center_urls
from libs.application import Application as myapplication
from biz.tasks.handlers.accept_task import accept_task_urls

class Application(myapplication):
    def __init__(self, **settings):
        urls = []

        urls.extend(accept_task_urls)
        super(Application, self).__init__(urls, **settings)

if __name__ == '__main__':
    pass
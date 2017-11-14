#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author :
date   : 2017/7/11 下午1:21
role   : Version Update
'''


from biz.tasks.exec_sched import DealMQ


class Application(DealMQ):
    def __init__(self, **settings):
        #configs.import_dict(**settings)
        super(Application, self).__init__()

    def start_server(self):
        self.start_consuming()

if __name__ == '__main__':
    app = Application()
    app.start_server()
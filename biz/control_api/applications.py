#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : task center
'''
class Application(VmbApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(list_urls)
        urls.extend(exception_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
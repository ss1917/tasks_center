#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:58:26
role   : 配置文件
'''

import os

from libs.consts import const

ROOT_DIR = os.path.dirname(__file__)

debug = True
xsrf_cookies = False

cookie_secret = '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='
expire_seconds = 365 * 24 * 60 * 60

DEFAULT_DB_DBHOST = '192.168.1.92'
DEFAULT_DB_DBPORT = '3306'
DEFAULT_DB_DBUSER = 'root'
DEFAULT_DB_DBPWD = 'ljXrcyn7chaBU4F'
DEFAULT_DB_DBNAME = 'shenshuo'

READONLY_DB_DBHOST = '192.168.1.92'
READONLY_DB_DBPORT = '3306'
READONLY_DB_DBUSER = 'root'
READONLY_DB_DBPWD = 'ljXrcyn7chaBU4F'
READONLY_DB_DBNAME = 'shenshuo'

DEFAULT_MQ_ADDR = '192.168.1.67'
DEFAULT_MQ_PORT = 56720
DEFAULT_MQ_VHOST = '/'
DEFAULT_MQ_USER = 'yz'
DEFAULT_MQ_PWD = 'vuz84B2IkbEtXWF'

DEFAULT_REDIS_HOST = '192.168.1.35'
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 8
DEFAULT_REDIS_AUTH = True
DEFAULT_REDIS_CHARSET = 'utf-8'
DEFAULT_REDIS_PASSWORD = 'Vmobel135791'

try:
    from local_settings import *
except:
    pass

settings = dict(
    debug=debug,
    xsrf_cookies=xsrf_cookies,
    cookie_secret=cookie_secret,
    expire_seconds=expire_seconds,
    databases={
        const.DEFAULT_DB_KEY: {
            const.DBHOST_KEY: DEFAULT_DB_DBHOST,
            const.DBPORT_KEY: DEFAULT_DB_DBPORT,
            const.DBUSER_KEY: DEFAULT_DB_DBUSER,
            const.DBPWD_KEY: DEFAULT_DB_DBPWD,
            const.DBNAME_KEY: DEFAULT_DB_DBNAME,
        },
        const.READONLY_DB_KEY: {
            const.DBHOST_KEY: READONLY_DB_DBHOST,
            const.DBPORT_KEY: READONLY_DB_DBPORT,
            const.DBUSER_KEY: READONLY_DB_DBUSER,
            const.DBPWD_KEY: READONLY_DB_DBPWD,
            const.DBNAME_KEY: READONLY_DB_DBNAME,
        }
    },
    mqs={
        const.DEFAULT_MQ_KEY: {
            const.MQ_ADDR: DEFAULT_MQ_ADDR,
            const.MQ_PORT: DEFAULT_MQ_PORT,
            const.MQ_VHOST: DEFAULT_MQ_VHOST,
            const.MQ_USER: DEFAULT_MQ_USER,
            const.MQ_PWD: DEFAULT_MQ_PWD,
        }
    },
    redises={
        const.DEFAULT_RD_KEY: {
            const.RD_HOST_KEY: DEFAULT_REDIS_HOST,
            const.RD_PORT_KEY: DEFAULT_REDIS_PORT,
            const.RD_DB_KEY: DEFAULT_REDIS_DB,
            const.RD_AUTH_KEY: DEFAULT_REDIS_AUTH,
            const.RD_CHARSET_KEY: DEFAULT_REDIS_CHARSET,
            const.RD_PASSWORD_KEY: DEFAULT_REDIS_PASSWORD
        }
    },
    app_name='task_control_center'
)
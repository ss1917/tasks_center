#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2017/4/11 下午1:54
role   : Version Update
'''


class ConstError(TypeError):
    pass


class _const(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError("Can't rebind const (%s)" % name)
        if not name.isupper():
            raise ConstError("Const must be upper.")
        self.__dict__[name] = value


const = _const()

const.DB_CONFIG_ITEM = 'databases'
const.DBHOST_KEY = 'host'
const.DBPWD_KEY = 'pwd'
const.DBUSER_KEY = 'user'
const.DBNAME_KEY = 'name'
const.DBPORT_KEY = 'port'
const.SF_DB_KEY = 'vmobel'
const.DEFAULT_DB_KEY = 'default'
const.READONLY_DB_KEY = 'readonly'

const.REDIS_CONFIG_ITEM = 'redises'
const.RD_HOST_KEY = 'host'
const.RD_PORT_KEY = 'port'
const.RD_DB_KEY = 'db'
const.RD_AUTH_KEY = 'auth'
const.RD_CHARSET_KEY = 'charset'
const.RD_PASSWORD_KEY = 'password'
const.DEFAULT_RD_KEY = 'default'

const.MQ_CONFIG_ITEM = 'mqs'
const.MQ_ADDR = 'MQ_ADDR'
const.MQ_PORT = 'MQ_PORT'
const.MQ_VHOST = 'MQ_VHOST'
const.MQ_USER = 'MQ_USER'
const.MQ_PWD = 'MQ_PWD'
const.DEFAULT_MQ_KEY = 'default'

const.APP_NAME = 'app_name'
const.LOG_PATH = 'log_path'
const.LOG_BACKUP_COUNT = 'log_backup_count'
const.LOG_MAX_FILE_SIZE = 'log_max_filesize'

const.REQUEST_START_SIGNAL = 'request_start'
const.REQUEST_FINISHED_SIGNAL = 'request_finished'
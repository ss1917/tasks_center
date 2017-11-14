#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2017/3/22 下午2:21
role   : Version Update
'''

import logging

LOGGER_FORMAT = ('PROGRESS:%(progress_id) -3s %(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                 '-35s LINE.NO:%(lineno) -5d : %(message)s')

MSG_QUEUE_LOG_KEY = 'messagequeue'


class ProgressLogFilter(logging.Filter):
    def filter(self, record):
        if hasattr(logging, 'progress_id'):
            record.progress_id = logging.progress_id
        else:
            record.progress_id = ''
        return True


def get_logger():
    return logging.getLogger(MSG_QUEUE_LOG_KEY)


def init_logger():
    queue_logger = logging.getLogger(MSG_QUEUE_LOG_KEY)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(LOGGER_FORMAT))
    console.setLevel(logging.INFO)
    queue_logger.setLevel(logging.INFO)
    queue_logger.addHandler(console)
    queue_logger.addFilter(ProgressLogFilter())


Logger = get_logger()
#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017年10月17日17:23:19
role   : task control models
'''
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class TaskList(Base):
    __tablename__ = 'task_list'

    ### 任务详情表
    list_id = Column('list_id', Integer, primary_key=True, autoincrement=True)
    task_name = Column('task_name', String(50))
    task_type = Column('task_type', String(50))
    hosts = Column('hosts', Text())
    args = Column('args', Text())
    details = Column('details', Text())
    descript = Column('descript', Text())
    mark = Column('mark', String(10))
    memo = Column('memo', String(10))
    creator = Column('creator', String(50))
    approver = Column('approver', String(50))
    status = Column('status', String(5))
    schedule = Column('schedule', String(50))
    temp_id = Column('temp_id', String(12))
    ctime = Column('ctime', DateTime(), default=datetime.now)
    stime = Column('stime', DateTime())


class TaskSched(Base):
    __tablename__ = 'task_sched'

    ### 根据任务表和任务模板表生成此表
    ### 任务根据此表执行
    sched_id = Column('sched_id', Integer, primary_key=True, autoincrement=True)
    list_id = Column('list_id', String(11))
    task_group = Column('task_group', String(5))
    task_level = Column('task_level', String(5))
    task_name = Column('task_name', String(30))
    task_cmd = Column('task_cmd', String(250))
    task_args = Column('task_args', String(250))
    trigger = Column('trigger', String(10))
    exec_user = Column('exec_user', String(30))
    forc_ip = Column('forc_ip', String(18))
    exec_ip = Column('exec_ip', String(18))
    task_status = Column('task_status', String(5))

class TaskLog(Base):
    __tablename__ = 'task_log'

    ### 任务日志表
    log_id = Column('log_id', Integer, primary_key=True, autoincrement=True)
    list_id = Column('list_id', String(11))
    exec_ip = Column('exec_ip', String(18))
    task_group = Column('task_group', String(5))
    task_level = Column('task_level', String(5))
    task_log = Column('task_log', String(250))
    log_time = Column('log_time', DateTime(), default=datetime.now)

class TaskMonitor(Base):
    __tablename__ = 'task_monitor'

    ### 任务监控
    list_id = Column('list_id', Integer, primary_key=True, autoincrement=True)
    call_level = Column('call_level', String(5))
    call_info = Column('call_info', String(500))
    ctime = Column('ctime', DateTime(), default=datetime.now)

class CmdList(Base):
    __tablename__ = 'cmd_list'

    ### 命令表
    cmd_id = Column('cmd_id', Integer, primary_key=True, autoincrement=True)
    cmd_name   = Column('cmd_name', String(25),unique=True)
    command = Column('command',String(250))
    args = Column('args', String(250))
    forc_ip = Column('forc_ip', String(250))
    creator = Column('creator', String(30))
    ctime = Column('ctime', DateTime(), default=datetime.now)

class TempList(Base):
    __tablename__ = 'temp_list'

    ### 命令模板列表
    temp_id = Column('temp_id', Integer, primary_key=True, autoincrement=True)
    temp_name  = Column('temp_name', String(25),unique=True)
    creator = Column('creator', String(30))
    ctime = Column('ctime', DateTime(), default=datetime.now)
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)


class TempDetails(Base):
    __tablename__ = 'temp_details'

    ### 执行模板详情
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    temp_id = Column('temp_id', String(11))
    group = Column('group', String(5))
    level = Column('level', String(5))
    cmd_name = Column('cmd_name', String(25))
    command = Column('command', String(250))
    args = Column('args', String(250))
    trigger = Column('trigger', String(10))
    exec_user = Column('exec_user', String(20))
    forc_ip = Column('forc_ip', String(15))
    creator = Column('creator', String(30))
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)

class ArgsList(Base):
    __tablename__ = 'args_list'

    ### 参数对照表
    args_id = Column('args_id', Integer, primary_key=True, autoincrement=True)
    args_name = Column('args_name', String(25))
    args_self = Column('args_self', String(35))
    creator = Column('creator', String(30))
    utime = Column('utime', DateTime(), default=datetime.now, onupdate=datetime.now)

if __name__ == '__main__':
    pass
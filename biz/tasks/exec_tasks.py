#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : exec tasks
### 任务状态标记 0:新建,1:等待,2:运行中,3:完成,4:错误,5:手动
### 任务组按顺序触发，任务按预设触发，默认顺序执行
'''
import fire, sys
import multiprocessing
from ast import literal_eval
import time, re
import paramiko

from models.models import TaskList, TaskSched, TaskLog
from libs.db_context import DBContext

class MyExecute():
    def __init__(self, flow_id, group_id):
        self.flow_id = str(flow_id)
        self.group_id = str(group_id)
        with DBContext('readonly') as session:
            taskinfo = session.query(TaskList.hosts, TaskList.args).filter(TaskList.list_id == self.flow_id).one()

        self.all_exec_ip = literal_eval(taskinfo[0]).get(self.group_id,'')
        print(self.all_exec_ip)
        self.all_args_info = literal_eval(taskinfo[1])

    ### 检查订单是否已经完成，防止重复执行
    def check_list(self):
        with DBContext('readonly') as session:
            jindu = session.query(TaskList).filter(TaskList.list_id == self.flow_id).first().schedule

        if jindu == 'OK' or jindu == '100':
            print('The order status is finished !!!')
            sys.exit(10)

    ### 检查之前的执行组状态
    def check_group(self, gid='before'):
        with DBContext('readonly') as session:
            if gid == 'before':
                status = session.query(TaskSched.task_status).filter(TaskSched.list_id == self.flow_id,
                                                                     TaskSched.task_group < self.group_id).all()
            else:
                status = session.query(TaskSched.task_status).filter(TaskSched.list_id == self.flow_id).all()
            session.commit()
        for i in status:
            if i[0] != '3':
                return '4'
        return '3'

    ### 执行定时任务，修改任务可执行状态
    def exec_start(self):
        pass

    ### 解析参数
    def resolve_args(self, args):
        args_list = []
        all_args = ''

        if args:
            p_list = args.split(' ')
            for p in p_list:
                par_l = self.all_args_info.get(p, p).strip()
                if type(par_l) == "unicode":
                    par_l = par_l.encode('utf-8')
                args_list.append(par_l)
            all_args = ' '.join(args_list)
            ###解析FLOW_ID
            all_args = all_args.replace('FLOW_ID', self.flow_id)
            return all_args
        else:
            return all_args

    ### 执行任务函数
    def exec_task(self, **info):
        mycmd = info.get('task_cmd', '') + ' ' + info.get('task_args', '')
        myssh = paramiko.SSHClient()
        myssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if info.get('forc_ip', '') != '':
            real_ip = info.get('forc_ip', '127.0.0.1')
        else:
            real_ip = info.get('exec_ip', '127.0.0.1')
        myssh.connect(hostname=real_ip, username=info.get('exec_user', 'root'), port=info.get('exec_port', 22))
        ### 修改状态为运行中
        with DBContext('default') as session:
            session.query(TaskSched).filter(TaskSched.list_id == self.flow_id, TaskSched.task_group == self.group_id,
                                            TaskSched.task_level == info['task_level'],
                                            TaskSched.exec_ip == info['exec_ip']).update({TaskSched.task_status: '2'})
            session.commit()

        stdin, stdout, stderr = myssh.exec_command(mycmd)
        status = stdout.channel.recv_exit_status()

        if status == 0:
            real_status = '3'
            real_stdout = stdout
        else:
            real_status = '4'
            real_stdout = stderr

        ### 修改运行后的状态
        with DBContext('default') as session:
            session.query(TaskSched).filter(TaskSched.list_id == self.flow_id, TaskSched.task_group == self.group_id,
                                            TaskSched.task_level == info['task_level'],
                                            TaskSched.exec_ip == info['exec_ip']).update({TaskSched.task_status: real_status})
            session.commit()

        ### 记录日志
        with DBContext('default') as session:
            for i in real_stdout.readlines():
                i = i.replace('\n', '')
                if i:
                    session.add(TaskLog(list_id=self.flow_id, task_group=self.group_id, task_level=info['task_level'],
                                        exec_ip=info['exec_ip'], task_log=i))

            session.commit()
            time.sleep(1)
        return real_status

    ### 任务调度函数
    ### 任务组按顺序触发，任务按预设触发，默认顺序执行
    def exec_main(self, ip):
        int_sleep = 0
        while True:
            ### 挂起的任务设置休眠时间
            print('list-{0} gourp-{1} perform sleep after {2} seconds'.format(self.flow_id, self.group_id, int_sleep))
            time.sleep(int_sleep)
            int_sleep += 1
            if int_sleep > 30:
                int_sleep = 30

            ### 检查订单状态
            if self.check_group('all') == '3':
                ### 修改订单进度以及退出循环
                break

            ### 如果之前执行组都成功，任务正式开始
            if self.check_group() == '3':
                level_list = []
                level_status = {}
                with DBContext('readonly') as session:
                    level_info = session.query(TaskSched).filter(TaskSched.list_id == self.flow_id, TaskSched.task_group
                                                                 == self.group_id, TaskSched.exec_ip == ip).all()

                for l in level_info:
                    level = l.task_level.replace('\n', '')
                    level_list.append(level)
                    level_status[level] = l.task_status
                level_list = sorted(level_list)

                for i in level_list:
                    cmd_info = session.query(TaskSched).filter(TaskSched.list_id == self.flow_id,
                                                                   TaskSched.task_group
                                                                   == self.group_id, TaskSched.task_level == i,
                                                                   TaskSched.exec_ip == ip).all()
                    session.commit()

                    for c in cmd_info:
                        cmd_trigger = c.trigger
                        exec_info = dict(
                            task_level=i,
                            task_name=c.task_name,
                            task_cmd=c.task_cmd,
                            task_args=self.resolve_args(c.task_args),
                            exec_user=c.exec_user,
                            forc_ip=c.forc_ip,
                            exec_ip=ip,
                        )

                    ### 如果没有定时触发器和手动触发器存在则退出本次循环
                    if cmd_trigger.replace('\n', '') in ['timed', 'hand']:
                        break

                    ### 当前状态为等待执行和当前执行队列没有失败
                    if level_status.get(i, '') == '1' and ('4' not in level_status.values()):
                        print('list-{0} {1} group-{2} level-{3} start'.format(self.flow_id, ip, self.group_id, i))
                        self.exec_task(**exec_info)
                        break

    ### 根据执行主机，并发执行任务调度
    def exec_thread(self):
        threads = []
        #####取所有IP###
        for ip in self.all_exec_ip:
            ip = ip.replace('\n', '').strip()

            ###并发调用execute函数
            ip_have = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', ip)
            if ip_have:
                threads.append(multiprocessing.Process(target=self.exec_main, args=(ip,)))

        print("current has {0} threads executive task list-{1} group-{2}" .format(len(threads),self.flow_id, self.group_id))

        ###开始多线程
        for start_t in threads:
            try:
                start_t.start()
            except UnboundLocalError:
                print('error')
        ###阻塞线程
        for join_t in threads:
            join_t.join()


def run(flow_id, group_id):
    ME = MyExecute(flow_id, group_id)
    ME.exec_thread()

if __name__ == "__main__":
    fire.Fire(run)

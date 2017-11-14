#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : SS
date   : 2017-10-11 12:48:43
role   : 接受任务API
'''
# import tornado.web
import json
from ast import literal_eval
from libs.mqhelper import MessageQueueBase
from biz.tasks.handlers.bash_handler import BaseHandler, LivenessProbe
from libs.db_context import DBContext
from models.models import TaskList, TaskSched, TempDetails, TempList


def new_task(list_id, temp_id, *group_list):
    '''根据订单和模板生成任务'''
    with DBContext('default') as session:
        ip_info = session.query(TaskList.hosts).filter(TaskList.list_id == list_id).one()

        for g in group_list:
            temp_info = session.query(TempDetails).filter(TempDetails.temp_id == temp_id, TempDetails.group == g).all()
            for ip in ip_info:
                ip = literal_eval(ip)
                gip = ip[g].split(',')
                for i in gip:
                    for t in temp_info:
                        session.add(
                            TaskSched(list_id=list_id, task_group=g, task_level=t.level, task_name=t.cmd_name, task_cmd=t.command,
                                      task_args=t.args, trigger=t.trigger, exec_user=t.exec_user, forc_ip=t.forc_ip, exec_ip=i,
                                      task_status='1'))

        session.commit()
        return 0


class AcceptTaskHandler(BaseHandler):
    def get(self, *args, **kwargs):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        ### 首先判断参数是否完整（temp_id，hosts，submitter）必填
        exec_time = data.get('exec_time', '2038-10-25 14:00:00')
        temp_id = str(data.get('temp_id', ''))
        task_type = data.get('task_type', '其他')
        submitter = data.get('submitter', '')  ### 应根据登录的用户
        approver = data.get('approver', '')  ### 审批人可以为空
        args = data.get('args', '')          ### 参数，可以为空
        hosts = data.get('hosts', '')        ### 执行主机，不能为空
        details = data.get('details', '')    ### 任务描述
        if hosts == '' or temp_id == '':
            json_data = {
                'status': '2',
                'msg': '主机和模板ID不能为空'
            }
            self.write(json_data)

        hosts = literal_eval(hosts)
        group_list = []
        hosts_dic = {}

        with DBContext('readonly') as session:
            all_group = session.query(TempDetails.group).filter(TempDetails.temp_id == temp_id).group_by(
                TempDetails.group).all()

            for g in all_group:
                g = g[0].strip()
                group_list.append(g)
                hosts_dic[g] = hosts.get(g, '')
            hosts_dic['main'] = hosts.get('main', '')

        if set(group_list).issubset(set(hosts.keys())) and 'main' in hosts.keys():
            with DBContext('default') as session:
                temp_name = session.query(TempList.temp_name).filter(TempList.temp_id == temp_id).one()
                new_list = TaskList(task_name=temp_name[0], task_type=task_type, hosts=str(hosts_dic), args=args, details=details,
                                    descript='', mark='', memo='', creator=submitter, approver=approver, status='0',
                                    schedule='new', temp_id=temp_id, stime=exec_time)
            session.add(new_list)
            session.commit()
            ### 最后生成任务，若没有接手和执行时间 等待接手和修改最终执行时间
            new_task(new_list.list_id, temp_id, *group_list)
            ### 发送消息
            with MessageQueueBase('task_sced', 'direct', 'the_task') as save_paper_channel:
                save_paper_channel.publish_message(str(new_list.list_id))

            json_data = {
                "list_id": new_list.list_id,
                "status": "0",
                "msg": "任务建立成功"
            }
            self.write(json_data)
        else:
            json_data = {
                "status": "3",
                "msg": "主机分组和模板分组不匹配"
            }
            self.write(json_data)

accept_task_urls = [
    (r"/v1/accept_task/", AcceptTaskHandler),
    (r"/", LivenessProbe)
]
if __name__ == "__main__":
    pass

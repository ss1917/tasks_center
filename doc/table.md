```
### 创建数据库
CREATE DATABASE `shenshuo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

##### 任务列表

  CREATE TABLE `task_list` (
  `list_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(50) NOT NULL,
  `task_type` varchar(50) NOT NULL,
  `hosts` longtext NOT NULL,
  `args` longtext NOT NULL,
  `details` longtext NOT NULL,
  `descript` varchar(25) NOT NULL,
  `mark` varchar(5) NOT NULL,
  `memo` varchar(10) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `approver` varchar(50) NOT NULL,
  `status` varchar(5) NOT NULL,
  `schedule` varchar(50) NOT NULL,
  `temp_id` varchar(12) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `stime` datetime DEFAULT NULL,
  PRIMARY KEY (`list_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8

##### 任务日志表

CREATE TABLE `task_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `list_id` varchar(11) NOT NULL,
  `task_group` varchar(5) NOT NULL,
  `task_level` varchar(5) NOT NULL,
  `exec_ip` char(15) NOT NULL,
  `task_log` varchar(250) NOT NULL,
  `log_time` datetime DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8

##### 任务调度表

CREATE TABLE `task_sched` (
  `sched_id` int(11) NOT NULL AUTO_INCREMENT,
  `list_id` varchar(11) NOT NULL,
  `task_group` varchar(5) NOT NULL,
  `task_level` varchar(5) NOT NULL,
  `task_name` varchar(25) NOT NULL,
  `task_cmd` varchar(128) NOT NULL,
  `task_args` varchar(128) NOT NULL,
  `trigger` varchar(10) NOT NULL,
  `exec_user` varchar(20) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `exec_ip` char(15) NOT NULL,
  `task_status` varchar(5) NOT NULL,
  PRIMARY KEY (`sched_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8

##### 命令表

 CREATE TABLE `cmd_list` (
  `cmd_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmd_name` varchar(25) NOT NULL,
  `command` varchar(250) NOT NULL,
  `args` varchar(250) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`cmd_id`)
) DEFAULT CHARSET=utf8;


##### 模板列表

 CREATE TABLE `temp_list` (
  `temp_id` int(11) NOT NULL AUTO_INCREMENT,
  `temp_name` varchar(25) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `ctime` datetime DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`temp_id`)
) DEFAULT CHARSET=utf8;


#####  模板详情

 CREATE TABLE `temp_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `temp_id` varchar(11) NOT NULL,
  `group` varchar(30) NOT NULL,
  `level` varchar(30) NOT NULL,
  `cmd_name` varchar(30) NOT NULL,
  `command` varchar(128) NOT NULL,
  `args` varchar(128) NOT NULL,
  `trigger` varchar(10) NOT NULL,
  `exec_user` varchar(20) NOT NULL,
  `forc_ip` char(15) NOT NULL,
  `creator` varchar(30) NOT NULL,
  `utime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8;
```
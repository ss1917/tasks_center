[group:task_center]
programs=exec_task,accept_api

[program:accept_api]
command=python3 startup.py --service=accept_api --port=91%(process_num)02d
process_name=%(program_name)s_%(process_num)02d
numprocs=2
directory=/var/www
user=www
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/accept_api.log
loglevel=info
logfile_maxbytes=50MB
logfile_backups=3


[program:exec_task]
command=python3 startup.py --service=exec_task
process_name=%(program_name)s_%(process_num)02d
numprocs=50
directory=/var/www
user=www
autostart = true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/exec_task.log
loglevel=info
logfile_maxbytes=50MB
logfile_backups=3
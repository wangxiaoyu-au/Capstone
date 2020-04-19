from fabric import task
from fabric import *
from fabric import SerialGroup as Group
from pathlib import Path
import os
import json
from benedict import benedict
from datetime import datetime, timedelta
import time


def get_config(filename):
    return os.path.join(Path(__file__).resolve().parent.parent, "config", filename)


def get_app_config(app_config="app.yaml"):
    app_cfg = get_config(app_config)
    print("Loading", app_cfg)
    return benedict.from_yaml(app_cfg)


@task
def start(ctx, task_name = 'noname', port_forward='portforward.yaml',app_config="app.yaml", duration=300):
    """

    duration seconds, 0 means no end time. Else put a duration here for monitoring, such if you want to launch monitoring for 10 minutes, put 600 here.
    """
    app_cfg = get_app_config(app_config)
    group = get_hosts(ctx, port_forward)
    
    # start time, end time
    now = datetime.now()
    if duration<=0:
        duration = 9999999 
    endtime = now + timedelta(seconds=duration)
    
    # monitoring data file
    monitor_file = now.strftime("%Y-%m-%d-%H-%M")
    monitor_group = 0
    period = app_cfg['perf']['period']
    interval = app_cfg['perf']['interval']

    while now < endtime:
        for c in group:
            output_file = task_name + "-" + monitor_file + "-" + "group" +  str(monitor_group)
            perf(ctx, output_file, interval, period)
        print("Sleep ", period, "seconds")
        time.sleep(period)
        for c in group:
            output_file = task_name + "-" + monitor_file + "-" + "group" +  str(monitor_group)
            get_remote_file(ctx, output_file, app_cfg['local'], app_cfg['hdfs'])

        monitor_group += 1
        now = datetime.now()
        print("Next loop", monitor_group)

    print("monitoring finished.")


@task
def get_hosts(ctx,port_forward='portforward.yaml'):
    hosts = []
    # Get mapping ports
    config_file = get_config(port_forward)
    print("Loading", config_file)
    ports = benedict.from_yaml(config_file)
    private_key = get_config(os.path.join('private_key', ports['key']))
    for port, ip in ports['mapping'].items():
        hosts.append('localhost:' + str(ip))

    print("user", ports['username'], "key_filename", private_key)

    return hosts
    # return Group(*hosts, user = ports['username'], connect_kwargs = {"key_filename":private_key})  


@task
def perf(ctx, output_file,  interval, period):
    perf_cmd_template = "perf -period {period} -output {output_file} -inteval {interval}"
    perf_cmd =  perf_cmd_template.format(
        output_file = output_file,
        interval = interval,
        period = period * 1000 # seconds to milliseconds
    )
    print("run: ", perf_cmd)
    # TODO: to implement


def get_remote_file(ctx, remote_file, local_folder, hdfs):
    print("copy remote %s to local %s ".format(remote_file, local_folder))
    print("uploading to HDFS %s ".format(hdfs))
    # TODO: to implement


@task
def report(ctx, task_name, date='today'):
    print("Reading perf file for task", task_name, date)
    

    


from fabric import task
from fabric import *
from fabric import SerialGroup as Group
from pathlib import Path
import os
import json
import yaml
import subprocess
from benedict import benedict
import psutil 
import tempfile
from datetime import datetime

def get_local_path(filename, dir='config'):
    return os.path.join(Path(__file__).resolve().parent.parent.parent, dir, filename)

def read_config(filename):
    config_file = get_local_path(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)


@task
def install(ctx, portforward='portforward.yaml', influxdb='y', grafana='y'):
    cfg = read_config(portforward)
    private_key = get_local_path(os.path.join('private_key', cfg['key']))
    if influxdb == 'y':
        conn_influx  = Connection(cfg['influxdb']['ip'], user = cfg['username'], connect_kwargs = {"key_filename":private_key})
        install_influxdb(conn_influx, cfg)
        

    if grafana == 'y':
        conn_grafana  = Connection(cfg['grafana']['ip'], user = cfg['username'], connect_kwargs = {"key_filename":private_key})
        install_grafana(conn_grafana)


def install_influxdb(ctx, cfg):
    print("Install InfluxDB ")
    ctx.run("hostname")
    ctx.run("echo \"deb https://repos.influxdata.com/ubuntu bionic stable\" | sudo tee /etc/apt/sources.list.d/influxdb.list")
    ctx.run("sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -")
    ctx.run("sudo apt update")
    ctx.run("sudo apt install -y influxdb")
    print("Installation complete")

def update_influxdb(ctx, cfg):
    ctx.run("sudo service influxdb stop")
    
    tmp = tempfile.TemporaryFile(mode='w+t')
    try:
        lines = open(get_local_path(cfg['influxdb']['config'])).readlines()
        lines = [ line.replace("{influxdb.port}", cfg['influxdb']['port']) for line in lines ]
        tmp.writelines(lines)
    finally:
        f.close()
    
    backup_file = "influxdb.conf.backup." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    local_backup = get_local_path(backup_file, 'backup')
    ctx.run("mkdir -p /home/" +  cfg['username'] + "/backup")
    remote_backup = "/home/" + cfg['username']  + "/backup/" + backup_file
    ctx.run("sudo cp /etc/influxdb/influxdb.conf " + remote_backup)
    ctx.run("sudo rm -rf /etc/influxdb/influxdb.conf")
    ctx.run("sudo chown " + cfg['username'] + ":"+ cfg['username'] + " " + remote_backup)
    ctx.get(remote_backup, local_backup)   

    new_file = "influxdb.conf.new." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    ctx.put(tmp.name, remote='/tmp/' + new_file)
    ctx.run("sudo cp /tmp/" + new_file + " /etc/influxdb/influxdb.conf")
    ctx.run("sudo service influxdb start")

def install_grafana(ctx):
    pass



@task
def install_grafana(ctx, portforward='portforward.yaml'):
    pass

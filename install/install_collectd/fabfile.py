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


def install_collectd(ctx):
    ctx.sudo("apt update -y")
    ctx.sudo("apt install collectd -y")


def get_local_path(filename, dir='config'):
    return os.path.join(Path(__file__).resolve().parent.parent.parent, dir, filename)

def read_config(filename):
    config_file = get_local_path(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)


def get_all_hosts(ctx, cfg):
    hosts = []
    # Get mapping ports
    private_key = get_local_path(os.path.join('private_key', cfg['key']))    
    for port in sorted(cfg['mapping'].keys()):
        hosts.append('localhost:' + str(port))
    print("user", cfg['username'], "key_filename", private_key)
    return Group(*hosts, user = cfg['username'], connect_kwargs = {"key_filename":private_key}) 


@task
def install(ctx, portforward='portforward.yaml'):
    cfg = read_config(portforward)
    hosts = get_all_hosts(ctx, cfg)
 
    master_port = sorted(cfg['mapping'].keys())[0]
    master_ip = cfg['mapping'][master_port]

    for host in hosts:
        install_collectd(host)

    start(ctx, portforward)

@task
def collectd_cmd(ctx, portforward='portforward.yaml', cmd="echo hello"):
    cfg = read_config(portforward)
    hosts = get_all_hosts(ctx, cfg) 
    for host in hosts: 
        host.run("hostname")
        host.run("echo \"" + cmd + "\"")
        host.run(cmd)


@task
def status(ctx, portforward='portforward.yaml'):
    collectd_cmd(ctx, portforward, 'ps aux | grep -v grep | grep collectd')


@task
def start(ctx, portforward='portforward.yaml'):
    collectd_cmd(ctx, portforward, 'sudo service collectd start')


@task
def stop(ctx, portforward='portforward.yaml'):
    collectd_cmd(ctx, portforward, 'sudo service collectd top')


@task
def update(ctx, portforward='portforward.yaml'):
    cfg = read_config(portforward)
    hosts = get_all_hosts(ctx, cfg)
    for host in hosts:
        update_collectd(host, cfg)


def update_collectd(ctx, cfg):
    ctx.run("sudo service collectd stop")

    tmp = tempfile.NamedTemporaryFile(mode='w+t', suffix=".conf", delete=False)
    try:
        lines = open(get_local_path(cfg['collectd']['config'])).readlines()
        lines = [ line.replace("{influxdb.ip}", str(cfg['influxdb']['ip'])) for line in lines ]
        lines = [ line.replace("{influxdb.port}", str(cfg['influxdb']['port'])) for line in lines ]
        tmp.writelines(lines)
    finally:
        tmp.close()
    
    backup_file = "collectd.conf.backup." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    local_backup = get_local_path(backup_file, 'backup')
    ctx.run("mkdir -p /home/" +  cfg['username'] + "/backup")
    remote_backup = "/home/" + cfg['username']  + "/backup/" + backup_file
    print("Backup remote: cp /etc/collectd/collectd.conf " + remote_backup)
    ctx.run("sudo cp /etc/collectd/collectd.conf " + remote_backup)
    ctx.run("sudo chown " + cfg['username'] + ":"+ cfg['username'] + " " + remote_backup)
    print("Download to local: " + local_backup)
    ctx.get(remote_backup, local_backup)   
   
    new_file = "/tmp/collectd.conf.new." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    print("Upload from local: " + str(tmp.name) + " to remote:" + new_file)
    ctx.put(str(tmp.name), remote= new_file)
    ctx.run("sudo rm -rf /etc/collectd/collectd.conf")
    ctx.run("sudo mv " +  new_file + " /etc/collectd/collectd.conf")
    print("Updated /etc/collectd/collectd.conf with " + new_file)
    ctx.run("sudo chown 644 /etc/collectd/collectd.conf")
    ctx.run("sudo service collectd start")
    ctx.run("hostname")
    print("Restart collectd complete")

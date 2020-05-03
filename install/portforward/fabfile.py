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


def get_config(filename):
    return os.path.join(Path(__file__).resolve().parent.parent.parent, "config", filename)

@task
def start(ctx, port_forward="portforward.yaml"):
    print("Using configurations", port_forward)
    config_file = get_config(port_forward)
    print("Loading", config_file)
    ports = benedict.from_yaml(config_file)
    private_key = get_config(os.path.join('private_key', ports['key']))
    for port, ip in ports['mapping'].items():
        map2local(ctx, ip, ports['username'], private_key, port )


@task
def stop(ctx):
    for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "ssh" in cmdline and "-fNL" in cmdline:
            print("Killing ", process.pid, cmdline)
            process.kill()


@task
def status(ctx):
    for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "ssh" in cmdline and "-fNL" in cmdline:
            print("Running ", process.pid, cmdline)


@task
def map2local(ctx, ip, username, keyfile, local_port, remote_port=22):
    cmd_template = 'ssh -oStrictHostKeyChecking=no -fNL {local_port}:localhost:{remote_port} {username}@{remote_ip}'
    print('Mapping', ip, ' on', remote_port, ' to localhost on', local_port)
    cmd = cmd_template.format(local_port=local_port,
        username=username,
        remote_port=remote_port,
        remote_ip=ip,
        keyfile=keyfile,
    )
    # Remove existing mapping
    subprocess.run('ssh-keygen -R [localhost]:{local_port}'.format(local_port=local_port).split(' '))
    subprocess.run(cmd.split(' '))

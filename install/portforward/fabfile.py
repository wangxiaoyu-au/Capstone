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

def read_config(filename):
    config_file = get_config(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)

def get_hosts(ctx, password, cfg):
    hosts = []
    # Get mapping ports
    for port, ip in cfg['mapping'].items():
        hosts.append(ip + ':22')
    print("user", cfg['username'])
    return Group(*hosts, user = cfg['username'], connect_kwargs={"password": password} )  

"""
fab --prompt-for-sudo-password init-sudo --port-forward=test.yaml --password= 
fab --prompt-for-sudo-password init-sudo --password= 
"""
@task
def init_sudo(ctx, password, port_forward="portforward.yaml"):
    cfg = read_config(port_forward)
    hosts = get_hosts(ctx, password, cfg)
    for h in hosts:
        # set_nopass_sudo(h, cfg)
        ssh_key_login(h, cfg)


def set_nopass_sudo(ctx, cfg):
    cmd = "echo '{0} ALL=(ALL) NOPASSWD: ALL' | sudo tee -a /etc/sudoers".format(cfg['username'])
    print(cmd)
    ctx.run(cmd)
    ctx.sudo("tail -1 /etc/sudoers")


def ssh_key_login(ctx, cfg):
    public_key = get_config(os.path.join('private_key', cfg['key'])) + '.pub'
    print("Using public key:", public_key)
    with open(public_key, "r") as f:
        print("Public key content:", public_key)
        ctx.run('mkdir -p ~/.ssh')
        ctx.run("hostname")
        ctx.run("echo '{0}' | tee -a ~/.ssh/authorized_keys".format(f.read()))
        ctx.run("chmod 400 ~/.ssh/authorized_keys")
        print("complete.")


@task
def start(ctx, port_forward="portforward.yaml", use_password='n'):
    print("Using configurations", port_forward)
    cfg = read_config(port_forward)
    private_key = get_config(os.path.join('private_key', cfg['key']))
    for port, ip in cfg['mapping'].items():
        map_to_local(ctx, ip, cfg['username'], private_key, port, use_password=use_password)

@task
def stop(ctx):
    for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "ssh" in cmdline and "-fNL" in cmdline:
            print("Killing: ", process.pid, cmdline)
            process.kill()


@task
def status(ctx):
    for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "ssh" in cmdline and "-fNL" in cmdline:
            print("Running: ", process.pid, cmdline)


@task
def map_to_local(ctx, ip, username, keyfile, local_port, remote_port=22, use_password='n'):
    cmd_template = 'ssh -oStrictHostKeyChecking=no -fNL {local_port}:localhost:{remote_port} {username}@{remote_ip}'
    if use_password == 'n':
        cmd_template += ' -i {keyfile}'
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

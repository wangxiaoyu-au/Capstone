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


@task
def connect(ctx):
    # install jdk8 test
    #C.run("sudo apt-get update")
    #C.run("sudo apt-get upgrade")
    #C.run("sudo apt-get install openjdk-8-jdk -y")

    # return the installed java version 
    #javaVersion = C.run("javac -version")

    # install spark test
    #C.run("mkdir software")
    #C.run("cd software")
    #C.run("sudo wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O software/spark-2.4.5-bin-hadoop2.7.tgz")
    #C.run("cd software && tar -xvf spark-2.4.5-bin-hadoop2.7.tgz")
    #C.run("sudo echo \"SPARK_HOME=/home/wangxiaoyu.au/software/spark-2.4.5-bin-hadoop2.7\" | sudo tee -a /etc/environment")
    
    # install scala test
    # C.run("sudo wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.deb -O software/scala-2.12.8.deb")
    # C.run("cd software && sudo dpkg -i scala-2.12.8.deb")
    # C.run("$SPARK_HOME/bin/spark-shell")
    # C.run("echo \"PATH=$PATH:$SPARK_HOME/bin\" >> ~/.bashrc") 
    # C.run("source ~/.bashrc")
    #C.run("mkdir /home/wangxiaoyu.au/MySparkConf")
    #C.put('C:/Projects/test_1/spark.master.conf', '/home/wangxiaoyu.au/MySparkConf/spark.master.conf')


@task
def install_jdk8(ctx):
    ctx.sudo("apt-get update -y")
    ctx.sudo("apt-get upgrade -y")
    ctx.sudo("apt-get install openjdk-8-jdk -y")
    ctx.run("javac -version") 


@task 
def install_spark(ctx, master_ip):
    ctx.sudo("apt-get remove scala-library scala")
    ctx.run("mkdir software")
    ctx.run("wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O software/spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("cd software && tar -xvf spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("echo 'SPARK_HOME=/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7' >> ~/.bashrc")
    ctx.run("echo 'PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc") 
    ctx.run("cp /home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh.template /home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh")
    ctx.run("echo 'export SPARK_MASTER_HOST=\"" + master_ip + "\"' >> /home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh")
    

@task
def install_scala(ctx):
    ctx.run("wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.deb -O software/scala-2.12.8.deb")
    ctx.run("cd software && sudo dpkg -i scala-2.12.8.deb")   

@task
def pool_test(ctx):
    ctx.run("hostname")
    print("--*--*--*--")


@task
def spark_master_action(ctx, action):
    ctx.run("/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/sbin/" + action + "-master.sh")
    # ctx.run("$SPARK_HOME/sbin/start-master.sh")


@task
def spark_workers_action(ctx, action, master_ip)):
    ctx.run("/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/sbin/" + action + "-slave.sh spark://" + master_ip + ":7077")


@task
def install_perf(ctx):
    ctx.sudo("apt install linux-tools-$(uname -r) linux-tools-generic -y")

@task
def install_mysql(ctx):
    ctx.sudo("apt-get update")
    ctx.sudo("apt-get install mysql-server -y")
    ctx.run("mysql --version")


def get_config_path(filename):
    return os.path.join(Path(__file__).resolve().parent.parent.parent, "config", filename)


def read_config(filename):
    config_file = get_config_path(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)


def get_spark_hosts(ctx, cfg):
    hosts = []
    # Get mapping ports
    private_key = get_config_path(os.path.join('private_key', cfg['key']))
    spark_range = cfg['spark-port-range']
    port_start = int(spark_range.split('-')[0])
    port_end = int(spark_range.split('-')[1])
    
    for port in sroted(cfg['mapping'].keys()):
        if port >= port_start and port <= port_end:
            hosts.append('localhost:' + str(port))
    print("user", cfg['username'], "key_filename", private_key)
    return Group(*hosts, user = cfg['username'], connect_kwargs = {"key_filename":private_key}) 


@task
def install(ctx, portforward='portforward.yaml'):
    cfg = read_config(portforward)
    hosts = get_spark_hosts(ctx, cfg)
 
    master_port = sorted(cfg['mapping'].keys())[0]
    master_ip = cfg['mapping'][master_port]

    for host in hosts:
        pool_test(c)
        install_jdk8(c)
        install_spark(c, master_ip)
        install_scala(c)
        install_perf(c)

    spark_action(ctx, portforward, 'start')

@task
def spark_action(ctx, portforward='portforward.yaml', action):
    cfg = read_config(portforward)
    hosts = get_spark_hosts(ctx, cfg) 
    master_port = sorted(cfg['mapping'].keys())[0]
    master_ip = cfg['mapping'][master_port]

    spark_master_action(hosts[0], 'start')   

    for host in hosts[1:]: 
        spark_workers_action(host, 'start', master_ip)


@task
def start_spark(ctx, portforward='portforward.yaml', action):
    spark_action(ctx, portforward, 'start')

@task
def stop_spark(ctx, portforward='portforward.yaml', action):
    spark_action(ctx, portforward, 'stop')

@task
def pip(ctx, package, portforward='portforward.yaml'):
    cfg = read_config(portforward)
    hosts = get_spark_hosts(ctx, cfg)
 
    for host in hosts:
        host.run("sudo apt install python3-pip -y")
        host.run("pip3 install {0} --user".format(package))

from fabric import task
from fabric import *
from fabric import SerialGroup as Group
import gcloud
import local
from pathlib import Path
import os
import json

@task
def deploy(ctx):
    print("Hello")

@task
def connect(ctx):
    with Connection(
        '34.82.46.2',        
        user = "wangxiaoyu.au", 
        connect_kwargs = {"key_filename":"C:/Capstone5709/newPrivateKey"}
        ) as C:

        # connection building test
        C.run('whoami')
        
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

def map_gcloud():
    #print("Calling Google API...")
    instances = gcloud.get_google_instances('mycapstoneprojectstest','us-west1-b')
    #print("\nGoogle Cloud instances:", instances, "\n")
    
    #print("Creating local mapping...")
    private_key_path = os.path.join(str(Path.home()), '.ssh', 'newPrivateKey')
    maps = local.create_local_port_forwarding(instances, 'wangxiaoyu.au', private_key_path, 10000)
    #print("\nRemote hosts with local mappings:", json.dumps(maps, indent=2), "\n")
    return instances, maps
        
@task
def install_jdk8(ctx):
    ctx.sudo("apt-get update -y")
    ctx.sudo("apt-get upgrade -y")
    ctx.sudo("apt-get install openjdk-8-jdk -y")
    ctx.run("javac -version") 

@task 
def install_spark(ctx):
    ctx.sudo("apt-get remove scala-library scala")
    ctx.run("mkdir software")
    ctx.run("wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O software/spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("cd software && tar -xvf spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("echo 'SPARK_HOME=/home/wangxiaoyu.au/software/spark-2.4.5-bin-hadoop2.7' >> ~/.bashrc")
    ctx.run("echo 'PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc") 
    ctx.run("source ~/.bashrc")
    ctx.run("export SPARK_HOME=/home/wangxiaoyu.au/software/spark-2.4.5-bin-hadoop2.7")
    ctx.run("export PATH=$PATH:$SPARK_HOME/bin")

@task
def install_scala(ctx):
    ctx.run("wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.deb -O software/scala-2.12.8.deb")
    ctx.run("cd software && sudo dpkg -i scala-2.12.8.deb")   

@task
def pool_test(ctx):
    ctx.run("whoami")
    print("---------")

@task
def spark_master_config(ctx):
    ctx.run("rm -rf /home/wangxiaoyu.au/MySparkConf")
    ctx.run("mkdir /home/wangxiaoyu.au/MySparkConf")
    ctx.put('C:/Projects/test_1/spark.master.conf', '/home/wangxiaoyu.au/MySparkConf/spark.master.conf')

# @task
# def spark_workers_config(ctx):
#     ctx.run("rm -rf /home/wangxiaoyu.au/MySparkConf")
#     ctx.run("mkdir /home/wangxiaoyu.au/MySparkConf")
#     ctx.put('C:/Projects/test_1/spark.workers.conf', '/home/wangxiaoyu.au/MySparkConf/spark.workers.conf')

@task
def spark_master_launch(ctx):
    ctx.run("/home/wangxiaoyu.au/software/spark-2.4.5-bin-hadoop2.7/sbin/start-master.sh")
    # ctx.run("$SPARK_HOME/sbin/start-master.sh")

@task
def spark_workers_launch(ctx):
    instances, maps = map_gcloud()
    internal_IP = instances[0]["internal_ip"]
    # ctx.run("$SPARK_HOME/sbin/start-slave.sh spark://" + internal_IP + ":7077")
    ctx.run("/home/wangxiaoyu.au/software/spark-2.4.5-bin-hadoop2.7/sbin/start-slave.sh spark://" + internal_IP + ":7077")


if __name__ == "__main__":   

    g_instances, g_maps = map_gcloud()
    print("g_instances:\n", g_instances)
    print()

    hosts = []
    for i in range(len(g_instances)):
        portnum = 10000 + i
        hosts.append('localhost:' + str(portnum))

    # print("host list:\n", hosts)
    # print()

    # print("Internal_IP:\n", g_instances[0]["internal_ip"])

    private_key_path = os.path.join(str(Path.home()), '.ssh', 'newPrivateKey')
    pool = Group(*hosts,
            user = "wangxiaoyu.au", 
            connect_kwargs = {"key_filename":private_key_path})  

    for c in pool:
        c.run("hostname")
    #     # # pool_test(c)
        install_jdk8(c)
        install_spark(c)
        install_scala(c)
        
    spark_master_config(pool[0])
    spark_master_launch(pool[0])   
    for c in pool[1:]: 
        spark_workers_launch(c)
    
    # for c in pool[1:]: 
    #     # spark_workers_launch(c)
    #     c.run("$SPARK_HOME/sbin/stop-slave.sh")
    # pool[0].run("$SPARK_HOME/sbin/stop-master.sh")
    
    

    
    

    


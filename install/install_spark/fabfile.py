from fabric import task
from fabric import *
from fabric import SerialGroup as Group
from pathlib import Path
import os
import json

@task
def connect(ctx):
    with Connection(
        '127.0.0.1:10002', 
        # port = 10000,     
        user = "xiaoyu",
        connect_kwargs={"password": "1"}        
        ) as C:

        # connection building test
        C.run("hostname")    
        
        # install MySQL
        install_mysql(C)
            
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
def install_spark(ctx):
    ctx.sudo("apt-get remove scala-library scala")
    ctx.run("mkdir software")
    ctx.run("wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O software/spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("cd software && tar -xvf spark-2.4.5-bin-hadoop2.7.tgz")
    ctx.run("echo 'SPARK_HOME=/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7' >> ~/.bashrc")
    ctx.run("echo 'PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc") 
    

@task
def install_scala(ctx):
    ctx.run("wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.deb -O software/scala-2.12.8.deb")
    ctx.run("cd software && sudo dpkg -i scala-2.12.8.deb")   

@task
def pool_test(ctx):
    ctx.run("hostname")
    print("--*--*--*--")


@task
def spark_master_launch(ctx):
    ctx.run("/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/sbin/start-master.sh")
    # ctx.run("$SPARK_HOME/sbin/start-master.sh")

@task
def spark_workers_launch(ctx):
    ctx.run("/home/xiaoyu/software/spark-2.4.5-bin-hadoop2.7/sbin/start-slave.sh spark://" + "192.168.122.53:7077")

@task
def install_perf(ctx):
    ctx.sudo("apt install linux-tools-$(uname -r) linux-tools-generic -y")

@task
def install_mysql(ctx):
    ctx.sudo("apt-get update")
    ctx.sudo("apt-get install mysql-server -y")
    ctx.run("mysql --version")


if __name__ == "__main__":   

    hosts = []
    for i in range(5):
        portnum = 10000 + i
        hosts.append('localhost:' + str(portnum))

    pool = Group(*hosts,
            user = "xiaoyu",
            connect_kwargs={"password": "1"})  

    for c in pool:
        pool_test(c)
        install_jdk8(c)
        install_spark(c)
        install_scala(c)
        install_perf(c)
        
    spark_master_launch(pool[0])   
    for c in pool[1:]: 
        spark_workers_launch(c)
    
    # for c in pool[1:]: 
    #     spark_workers_launch(c)
    #     c.run("$SPARK_HOME/sbin/stop-slave.sh")
    # pool[0].run("$SPARK_HOME/sbin/stop-master.sh")
    
    

    
    

    


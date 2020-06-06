import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase
import os
from fabric import Group

class Spark(ControlBase):

    def _get_hosts(self, password=''):
        hosts = []
        # Get mapping ports
        private_key = self.get_local_path(os.path.join('private_key', self._config['key']))
        spark_range = self._config['spark-port-range']
        port_start = int(spark_range.split('-')[0])
        port_end = int(spark_range.split('-')[1])
        
        for port in sorted(self._config['mapping'].keys()):
            if port >= port_start and port <= port_end:
                hosts.append('localhost:' + str(port))
        print("user", self._config['username'], "key_filename", private_key)
        return Group(*hosts, user = self._config['username'], connect_kwargs = {"key_filename":private_key}) 


    def install(self, password=''):
        hosts = self._get_hosts(password)
        master_port = sorted(self._config['mapping'].keys())[0]
        master_ip = self._config['mapping'][master_port]

        for host in hosts:
            self._install(host, master_ip)


    def _install(self, host, master_ip):
        self.pool_test(host)
        self.install_jdk8(host)
        self.install_spark(host, master_ip)
        self.install_scala(host)
        self.install_perf(host)

    def pool_test(self, host):
        host.run("hostname")
        print("--*--*--*--")

    def install_jdk8(self, host):
        host.sudo("apt-get update -y")
        host.sudo("apt-get upgrade -y")
        host.sudo("apt-get install openjdk-8-jdk -y")
        host.run("javac -version") 

    def install_spark(self, host, master_ip):
        host.sudo("apt-get remove scala-library scala")
        host.run("mkdir software")
        host.run("wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz -O software/spark-2.4.5-bin-hadoop2.7.tgz")
        host.run("cd software && tar -xvf spark-2.4.5-bin-hadoop2.7.tgz")
        host.run("echo 'SPARK_HOME=/home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7' >> ~/.bashrc")
        host.run("echo 'PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc") 
        host.run("cp /home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh.template /home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh")
        host.run("echo 'export SPARK_MASTER_HOST=\"" + master_ip + "\"' >> /home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7/conf/spark-env.sh")
        
    def install_scala(self, host):
        host.run("wget https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.deb -O software/scala-2.12.8.deb")
        host.run("cd software && sudo dpkg -i scala-2.12.8.deb")   


    def install_perf(self, host):
        host.sudo("apt install linux-tools-$(uname -r) linux-tools-generic -y")


    def _spark_action(self, action='start'):
        hosts = self._get_hosts()
        master_port = sorted(self._config['mapping'].keys())[0]
        master_ip = self._config['mapping'][master_port]

        self._spark_master_action(hosts[0], action)   

        for host in hosts[1:]: 
            self._spark_workers_action(host, action, master_ip)


    def _spark_master_action(self, host, action):
        host.run("hostname")
        host.run("/home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7/sbin/" + action + "-master.sh")


    def _spark_workers_action(self, host, action, master_ip):
        host.run("hostname")
        host.run("/home/"+self._config['username']+"/software/spark-2.4.5-bin-hadoop2.7/sbin/" + action + "-slave.sh spark://" + master_ip + ":7077")


    def start(self):
        self._spark_action('start')


    def stop(self):
        self._spark_action('stop')


    def _status(self, host):
        host.run('ps aux | grep -v grep | grep spark')
   

    def _update(self, host):
        print("Nothing need to be updated")

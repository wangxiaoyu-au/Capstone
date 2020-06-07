import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase
import os
from fabric import Group


class Hdfs(ControlBase):

    def _get_hosts(self, password=''):
        private_key = self.get_local_path(os.path.join('private_key', self._config['key']))
        hosts = []
        hdfs = self._config['hdfs']
        # First is master
        hosts.append(hdfs['master'] + ":22")
        for name, ip in hdfs.items():
            if name != 'master':
                hosts.append(ip + ":22")

        return Group(*hosts, user = self._config['username'], connect_kwargs = {"key_filename":private_key})


    def install(self, password=''):
        hosts = self._get_hosts()
        master_pub_key = self._init_master(hosts[0])

        for host in hosts: 
            self._install_hadoop(host, master_pub_key)

        self.update()

        hosts[0].run("/usr/local/hadoop/bin/hdfs namenode -format")


    def _init_master(self, host):
        print("Install master, generating keys")
        host.run("ssh-keygen -b 4096")
        local_pub = "/tmp/hadoop_master_pub_" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        host.get("~/.ssh/id_rsa.pub", local_pub)
        with open(local_pub, 'r') as myfile:
            return myfile.read() 


    def _install_hadoop(self, host, master_pub_key):
        host.run("sudo apt update -y")
        host.run("sudo apt install default-jdk wget -y")

        host.run("wget https://downloads.apache.org/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz")
        host.run("tar -xzvf hadoop-3.1.3.tar.gz")
        host.run("sudo mv hadoop-3.1.3 /usr/local/hadoop")
        host.run("java_home=$(readlink -f /usr/bin/java | sed \"s:bin/java::\")")
        host.run("echo \"export JAVA_HOME=${java_home}\" | sudo tee -a /usr/local/hadoop/etc/hadoop/hadoop-env.sh")

        host.run("sudo mkdir /hadoop")
        host.run("sudo mkdir /hadoop/data")
        host.run("sudo chown $(id -u):$(id -g) -R /hadoop")
        host.run("sudo chmod 777  /hadoop")
        host.run("sudo mkdir /usr/local/hadoop/logs")
        host.run("sudo chown $(id -u):$(id -g) -R /usr/local/hadoop/logs")

        host.run("echo \""  + master_pub_key +  "\" >>  ~/.ssh/authorized_keys")


    def start(self):
        hosts = self._get_hosts()
        hosts[0].run('/usr/local/hadoop/sbin/start-dfs.sh')


    def status(self):
        hosts = self._get_hosts()
        hosts[0].run('jps')
        hosts[0].run('/usr/local/hadoop/bin/hdfs dfsadmin -report')


    def stop(self):
        hosts = self._get_hosts()
        hosts[0].run('/usr/local/hadoop/sbin/stop-dfs.sh')


    def update(self):
        hosts = self._get_hosts()
        master_ip = self._config['hdfs']['master']
        for host in hosts:
            self._upload(host, "hadoop/core-site.xml.template", "/usr/local/hadoop/etc/hadoop/core-site.xml", master_ip)
            self._upload(host, "hadoop/hdfs-site.xml.template", "/usr/local/hadoop/etc/hadoop/hdfs-site.xml", master_ip)
            self._upload(host, "hadoop/mapred-site.xml.template", "/usr/local/hadoop/etc/hadoop/mapred-site.xml", master_ip)
            self._upload(host, "hadoop/yarn-site.xml.template", "/usr/local/hadoop/etc/hadoop/yarn-site.xml", master_ip)

        print("Updating /usr/local/hadoop/etc/hadoop/workers")
        hosts[0].run("sudo rm -f /usr/local/hadoop/etc/hadoop/workers.backup")
        hosts[0].run("sudo mv /usr/local/hadoop/etc/hadoop/workers /usr/local/hadoop/etc/hadoop/workers.backup")
        for ip in self._config['hdfs'].values():
            hosts[0].run("echo " + ip + " >> /usr/local/hadoop/etc/hadoop/workers")


    def _upload(self, host, local_template, remote_file, master_ip):
        tmp = tempfile.NamedTemporaryFile(mode='w+t', suffix=".conf", delete=False)
        try:
            lines = open(self.get_local_path(local_template)).readlines()
            lines = [ line.replace("{master_ip}", master_ip) for line in lines ]
            tmp.writelines(lines)
        finally:
            tmp.close()
       
        print("Updating " + remote_file)
        host.run("sudo rm -f " + remote_file + ".backup")
        host.run("sudo mv {remote_file} {remote_file}.backup".format(remote_file=remote_file))
        
        new_file = "/tmp/template_file_" + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        host.put(str(tmp.name), remote=new_file)
        host.run("sudo mv " + new_file + " " + remote_file)
        host.run("sudo chown $(id -u):$(id -g) " + remote_file)


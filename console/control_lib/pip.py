import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase
import os
from fabric import Group

class Pip(ControlBase):

    def __init__(self, config):
        super().__init__(config)
        self._pip_packages = ['scikit-learn']

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


    def _install(self, host):
        host.run("sudo apt install python3-pip -y")
        for package in self._pip_packages:
            host.run("pip3 install {0} --user".format(package))


    def start(self):
        print("Nothing need to be started")


    def stop(self):
        print("Nothing need to be stopped")


    def status(self):
        print("Nothing need to be showed")


    def update(self):
        print("Nothing need to be updated")

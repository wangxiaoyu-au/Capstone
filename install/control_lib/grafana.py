import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase

class Grafana(ControlBase):

    def _get_hosts(self, password=''):
        private_key = self.get_local_path(os.path.join('private_key', self.config['key']))
        return [Connection(self.config['grafana']['ip'],
                    user = self.config['username'], 
                    connect_kwargs = {"key_filename":private_key})]


    def _install(self, host):
        print("Install Grafana ")
        host.run("hostname")
        host.run("sudo apt install -y apt-transport-https")
        host.run("sudo apt install -y software-properties-common wget")
        host.run("wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -")
        host.run("sudo add-apt-repository \"deb https://packages.grafana.com/oss/deb stable main\"")
        host.run("sudo apt update")
        host.run("sudo apt install grafana -y")
        host.run("sudo service grafana-server start")


    def _start(self, host):
        host.run('sudo service grafana-server start')


    def _status(self, host):
        host.run('ps aux | grep -v grep | grep grafana-server')


    def _stop(self, host):
        host.run('sudo service grafana-server stop')


    def _update(self, host):
        print("Nothing need to be updated")
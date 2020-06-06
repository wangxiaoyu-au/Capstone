import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase

class Influxdb(ControlBase):

    def _get_hosts(self, password=''):
        private_key = self.get_local_path(os.path.join('private_key', self._config['key']))
        return [Connection(self._config['influxdb']['ip'],
                    user = self._config['username'], 
                    connect_kwargs = {"key_filename":private_key})]


    def _install(self, host):
        print("Install InfluxDB ")
        host.run("hostname")
        host.run("echo \"deb https://repos.influxdata.com/ubuntu bionic stable\" | sudo tee /etc/apt/sources.list.d/influxdb.list")
        host.run("sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -")
        host.run("sudo apt update")
        host.run("sudo apt install -y influxdb")
        host.run("sudo mkdir /usr/share/collectd")
        host.run("sudo wget -P /usr/share/collectd https://raw.githubusercontent.com/collectd/collectd/master/src/types.db")
        host.run("sudo service influxdb start")
        print("Installation complete")


    def _start(self, host):
        host.run('sudo service influxdb start')


    def _status(self, host):
        host.run('ps aux | grep -v grep | grep influxdb')


    def _stop(self, host):
        host.run('sudo service influxdb stop')


    def _update(self, host):
        host.run("sudo service influxdb stop")

        tmp = tempfile.NamedTemporaryFile(mode='w+t', suffix=".conf", delete=False)
        try:
            lines = open(get_local_path(self._config['influxdb']['config'])).readlines()
            lines = [ line.replace("{influxdb.port}", str(self._config['influxdb']['port'])) for line in lines ]
            tmp.writelines(lines)
        finally:
            tmp.close()
        
        backup_file = "influxdb.conf.backup." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        local_backup = get_local_path(backup_file, 'backup')
        host.run("mkdir -p /home/" +  self._config['username'] + "/backup")
        remote_backup = "/home/" + self._config['username']  + "/backup/" + backup_file
        print("Backup remote: cp /etc/influxdb/influxdb.conf " + remote_backup)
        host.run("sudo cp /etc/influxdb/influxdb.conf " + remote_backup)
        host.run("sudo chown " + self._config['username'] + ":"+ self._config['username'] + " " + remote_backup)
        print("Download to local: " + local_backup)
        host.get(remote_backup, local_backup)   
    
        new_file = "/tmp/influxdb.conf.new." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        print("Upload from local: " + str(tmp.name) + " to remote:" + new_file)
        host.put(str(tmp.name), remote= new_file)
        host.run("sudo rm -rf /etc/influxdb/influxdb.conf")
        host.run("sudo mv " +  new_file + " /etc/influxdb/influxdb.conf")
        print("Updated /etc/influxdb/influxdb.conf with " + new_file)
        host.run("sudo chown influxdb:influxdb /etc/influxdb/influxdb.conf")
        host.run("sudo service influxdb start")
        print("Restart InfluxDB complete")
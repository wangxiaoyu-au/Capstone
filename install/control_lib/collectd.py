import tempfile
from datetime import datetime
from control_lib.control_base import ControlBase

class Collectd(ControlBase):

    def _install(self, host):
        host.sudo("apt update -y")
        host.sudo("apt install collectd -y")


    def _start(self, host):
        host.run('sudo service collectd start')


    def _status(self, host):
        host.run('ps aux | grep -v grep | grep collectd')


    def _stop(self, host):
        host.run('sudo service collectd start')


    def _update(self, host):
        host.run("sudo service collectd stop")

        tmp = tempfile.NamedTemporaryFile(mode='w+t', suffix=".conf", delete=False)
        try:
            lines = open(get_local_path(cfg['collectd']['config'])).readlines()
            lines = [ line.replace("{influxdb.ip}", str(cfg['influxdb']['ip'])) for line in lines ]
            lines = [ line.replace("{influxdb.port}", str(cfg['influxdb']['port'])) for line in lines ]
            tmp.writelines(lines)
        finally:
            tmp.close()
    
        backup_file = "collectd.conf.backup." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        local_backup = self.get_local_path(backup_file, 'backup')
        host.run("mkdir -p /home/" +  cfg['username'] + "/backup")
        remote_backup = "/home/" + cfg['username']  + "/backup/" + backup_file
        print("Backup remote: cp /etc/collectd/collectd.conf " + remote_backup)
        host.run("sudo cp /etc/collectd/collectd.conf " + remote_backup)
        host.run("sudo chown " + cfg['username'] + ":"+ cfg['username'] + " " + remote_backup)
        print("Download to local: " + local_backup)
        host.get(remote_backup, local_backup)   
    
        new_file = "/tmp/collectd.conf.new." + datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        print("Upload from local: " + str(tmp.name) + " to remote:" + new_file)
        host.put(str(tmp.name), remote= new_file)
        host.run("sudo rm -rf /etc/collectd/collectd.conf")
        host.run("sudo mv " +  new_file + " /etc/collectd/collectd.conf")
        print("Updated /etc/collectd/collectd.conf with " + new_file)
        host.run("sudo chown 644 /etc/collectd/collectd.conf")
        host.run("sudo service collectd start")
        host.run("hostname")
        print("Restart collectd complete")
from benedict import benedict
from fabric import SerialGroup as Group
import os

class ControlBase:

    def __init__(self, config):
        self._config = config

    def get_local_path(self, filename, dir='config'):
        return os.path.join(Path(__file__).resolve().parent.parent.parent, dir, filename)

    def _get_hosts(self):
        """Get hosts from configuration"""
        hosts = []
        # Get mapping ports
        private_key = self.get_local_path(os.path.join('private_key', self._config['key']))    
        for port in sorted(self._config['mapping'].keys()):
            hosts.append('localhost:' + str(port))
        print("user", self._config['username'], "key_filename", private_key)
        return Group(*hosts, user = self._config['username'], connect_kwargs = {"key_filename":private_key}) 


    def _install(self, host):
        """Install software to all hosts."""
        pass


    def _start(self, host):
        """Start software on all hosts."""
        pass


    def _status(self, host):
        """Stop software on all hosts."""
        pass


    def _stop(self, host):
        """Stop software on all hosts."""
        pass


    def _update(self, host):
        """Extract text from the currently loaded file."""
        pass


    def install(self):
        hosts = self._get_hosts()
        for host in hosts:
            self._install(host)


    def start(self):
        hosts = self._get_hosts()
        for host in hosts:
            self._start(host)


    def status(self):
        hosts = self._get_hosts()
        for host in hosts:
            self._status(host)


    def stop(self):
        hosts = self._get_hosts()
        for host in hosts:
            self._update(host)


    def update(self):
        hosts = self._get_hosts()
        for host in hosts:
            self._update(host)
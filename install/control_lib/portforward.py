from control_lib.control_base import ControlBase
import subprocess
import psutil 

class Portforward(ControlBase):

    def _get_hosts(self, password=''):
        if password == '':
            raise Error("You have to use password to complete portforward module installation.") 
        hosts = []
        # Get mapping ports
        for port, ip in self.config['mapping'].items():
            hosts.append(ip + ':22')
        print("user", self.config['username'])
        return Group(*hosts, user = self.config['username'], connect_kwargs={"password": password} )  


    def _install(self, host):
        # self.__install_nopass_sudo() still have some issues
        self.__install_ssh_key_login(host)

    
    def __install_nopass_sudo(self, host):
        cmd = "echo '{0} ALL=(ALL) NOPASSWD: ALL' | sudo tee -a /etc/sudoers".format(self.config['username'])
        print(cmd)
        host.run(cmd)
        host.sudo("tail -1 /etc/sudoers")


    def __install_ssh_key_login(self, host):
        public_key = get_config_path(os.path.join('private_key', self.config['key'])) + '.pub'
        print("Using public key:", public_key)
        with open(public_key, "r") as f:
            print("Public key content:", public_key)
            host.run('mkdir -p ~/.ssh')
            host.run("hostname")
            host.run("echo '{0}' | tee -a ~/.ssh/authorized_keys".format(f.read()))
            host.run("chmod 400 ~/.ssh/authorized_keys")
            print("complete.")


    def start(self):
        private_key = get_config_path(os.path.join('private_key', self.config['key']))
        for port, ip in self.config['mapping'].items():
            self._map_to_local(ip, self.config['username'], private_key, port)


    def _map_to_local(self, ip, username, keyfile, local_port, remote_port=22, use_password='n'):
        cmd_template = 'ssh -oStrictHostKeyChecking=no -fNL {local_port}:localhost:{remote_port} {username}@{remote_ip}'
        if use_password == 'n':
            cmd_template += ' -i {keyfile}'
        print('Mapping', ip, ' on', remote_port, ' to localhost on', local_port)
        cmd = cmd_template.format(local_port=local_port,
            username=username,
            remote_port=remote_port,
            remote_ip=ip,
            keyfile=keyfile,
        )
        
        # Remove existing mapping
        subprocess.run('ssh-keygen -R "{remote_ip}"'.format(remote_ip=ip).split(' '))
        subprocess.run('ssh-keygen -R [localhost]:{local_port}'.format(local_port=local_port).split(' '))
        subprocess.run(cmd.split(' '))


    def stop(self):
        for process in psutil.process_iter():
            cmdline = process.cmdline()
            if "ssh" in cmdline and "-fNL" in cmdline:
                print("Killing: ", process.pid, cmdline)
                process.kill()


    def status(self):
        for process in psutil.process_iter():
            cmdline = process.cmdline()
            if "ssh" in cmdline and "-fNL" in cmdline:
                print("Running: ", process.pid, cmdline)


    def _update(self, host):
        print("Nothing need to be updated")
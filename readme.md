# Content

- `config` Configurations of IPs.
- `install` Install Spark, HDFS.
- `install/gcloud` Google cloud kits for port forwarding.
- `monitor` Start collecting monitoring data.
- `test_tasks` Testing spark tasks.

# Usage

## Initialise environment

Run following command to initialise the environment

```bash
virtualenv .fabenv --python=python3
```

Then install all dependencies

```bash
pip install -r dep.txt 
```

## Installation

### Preparation

Generating a private key before installlation for no password loging

```bash
ssh-keygen -t rsa -b 4096 -C "xiaoyu@usyd" -f config/private_key/dev_key
```

Copy the output of this command and run it in every host that need to login (e.g new Ubuntu OS)

echo "echo \"$(cat config/private_key/dev_key.pub)\" >> ~/.ssh/authorized_keys"

### No Password sudo

```
echo "${USER} ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
```

### System preparation (testing)

```
sudo apt install openjdk-8 openjdk-11 openjdk-11-dbg openjdk-8-dbg 
sudo apt install libelf-dev libunwind-dev libaudit-dev libclang-dev
```

### Install Spark

### Install HDFS

### Portforwarding

The configuration is located in `config/portforward.yaml`

```bash
cd install/portforward
fab start
fab stop
```

Also supports:

```bash
fab start "different-file.yaml"
```

## Monitoring

### Start Monitoring


Perf command line references:
* https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-record.txt
* http://www.brendangregg.com/perf.html
* https://perf.wiki.kernel.org/

Perf command line template can be configured in [app.yaml](config/app.yaml).

`period` is the parameter not just for dumping file to disk, but also for uploading files to HDFS.

```bash
fab start      # start perf
fab stop       # stop perf
fab status     # show perf status
```

Task name is the folder name that storing the perf.data in remote/local/HDFS

```bash
cd monitor
fab start # task name: noname
fab start --task-name=<task name>
fab start --duration=600 # 600 seconds, duration means monitoring for how long
fab start --duration=0 # default: 300 seconds, 0 means running all the time
fab report --task-name=<task name> --date=2020-01-20 # get perf monitoring data from HDFS to local
```

### Submit Test Spark Tasks







# Content

- `config` Configurations of IPs.
- `console` Install Portforward, Spark, Collectd, InfluxDB, Grafana, HDFS .
- `install/gcloud` Google cloud kits for port forwarding.
- `monitor` Start collecting Perf monitoring data.
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

```bash
echo "${USER} ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
```

### System preparation (testing)

```
sudo apt install openjdk-8 openjdk-11 openjdk-11-dbg openjdk-8-dbg 
sudo apt install libelf-dev libunwind-dev libaudit-dev libclang-dev
```

### Install Portforward/Spark/Collectd/InfluxDB/Grafana/HDFS

```bash
cd console
fab install # Install everything

# If install single module

fab install --module <module name>

# Such as 
fab install --module spark
fab install --module collectd
fab install --module grafana
fab install --module influxdb

# If install multiple moduels
fab install --module <module name1>,<module name2>,...

# Such as
fab install --module spark,collectd
```

## Enable Local Portforward

```bash
fab start --module portforward
```

## Configure InfluxDB

After installation, there are some manual steps need to be taken.

See http://www.inanzzz.com/index.php/post/ms6c/collectd-influxdb-and-grafana-integration

There are steps can't automated at this moment due to influxdb 1.8 is the stable version
https://docs.influxdata.com/influxdb/v1.8/tools/influx-cli/

InfluxDB 2.0 support commandline query https://v2.docs.influxdata.com/v2.0/reference/cli/influx/query

```bash
ssh xiaoyu@localhost -p 11000
# Please copy one line execute it then another line.
influx
# Change xxx to the influxdb password
CREATE USER influx_admin WITH PASSWORD 'xxx' WITH ALL PRIVILEGES
CREATE DATABASE collectd
exit
exit
```

## Update collectd & InfluxDB configuration

Configuration files are located in the configuration file are located in [config/*.conf.template](../config/).

```bash
fab update --module collectd,influxdb
```

## Stop & Start everything

```bash
fab stop
fab start
```

## Check module status

```bash
# Command
fab status --module <module name 1>,<module name 2>...
# Such as
fab status --module collectd
```

### Submit Test Spark Tasks

```bash
cd test_tasks
```

There are 6 tasks right now, execute `submit-*.sh` file to submit spark tasks

Such as:

```bash
cd spark_test_tasks2
./submit-2g-6-cores.sh
# Or
./submit-2.8g-all-cores.sh
```






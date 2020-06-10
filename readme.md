# Content

- `config` Configurations of IPs.
- `console` Install Portforward, Spark, Collectd, InfluxDB, Grafana, HDFS.
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

#### Step 0: Set up execution evnironment

```bash
source .fabenv/bin/activate
```

#### Step 1: Set up portforward

For new Spark cluster, update [config.yaml](config/config.yaml), then

```bash
cd console
fab install --module portforward
fab start --module portforward
```

#### Setp 2: Install Spark/Collectd/InfluxDB/Grafana
```
fab install --module spark,collectd,grafana,influxdb,pip,hdfs
```

#### Setp 3: Configure InfluxDB

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

#### Setp 4: Update collectd & InfluxDB configuration

Configuration files are located in the configuration file are located in [config/*.conf.template](../config/).

```bash
fab update --module collectd,influxdb
```

#### Setp 5: Stop & Start everything

```bash
fab stop --module spark,collectd,grafana,hdfs
fab start --module spark,collectd,grafana,influxdb,hdfs
```

#### Setp 6: Check module status

```bash
fab status

# Checking single or multiple module status
fab status --module <module name 1>,<module name 2>...
# Such as
fab status --module collectd
# Or
fab status --module influxdb,grafana
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

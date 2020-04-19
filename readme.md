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

### Install Spark

### Install HDFS

## Monitoring

### Start Monitoring



```bash
cd monitor
fab start
fab start --duration=600 # duration means monitoring for how long
```

### Submit Test Spark Tasks

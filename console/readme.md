Overview
========
Add new modules to use unified `fab install/start/stop/status/update` experience.

# Usage

## Install

```bash
# Install collectd using default configuration
fab install --module collectd
# Install Grafana using different configuration
fab install --module grafana --config-file another.yaml
# Enable Portforward, login with privatekey
fab install --module portforard
# Install pip and additional python modules
fab install --module pip
# Install Influxdb
fab install --module influxdb
# Install Spark
fab install --module spark
# Install HDFS
fab install --module hdfs
```

## Start

```bash
fab start --module collectd
fab start --module grafana
fab start --module influxdb
fab start --module spark
fab start --module portforward
```

## Stop

```bash
fab stop --module collectd
fab stop --module grafana
fab stop --module influxdb
fab stop --module spark
fab stop --module portforward
fab stop --module hdfs
```

## Status

```bash
fab status --module collectd
fab status --module grafana
fab status --module influxdb
fab status --module spark
fab status --module portforward
fab status --module hdfs
```


## Update

Update configurations, the configuration file are located in [config/*.conf.template](../config/).

```bash
fab update --module collectd
fab update --module influxdb
fab update --module hdfs
```
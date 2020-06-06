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
```

## Start

```
fab start --module collectd
fab start --module grafana
fab start --module influxdb
fab start --module spark
fab start --module portforward
```
```

## Stop

```
fab stop --module collectd
fab stop --module grafana
fab stop --module influxdb
fab stop --module spark
fab stop --module portforward
```

## Status

```
fab status --module collectd
fab status --module grafana
fab status --module influxdb
fab status --module spark
fab status --module portforward
```


## Update

Update configurations, the configuration file are located in [config/*.conf.template](../config/).

```
fab status --module collectd
fab status --module influxdb
```
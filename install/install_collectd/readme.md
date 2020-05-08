# Collectd Installation

## Prerequisite

1. Configure portforward.yaml first
1. [Lauch port forward](../portforward/readme.md)

## Usage

```bash
fab install # Install collectd
fab start # start collectd
fab stop  # stop collectd
```

## Update Collectd Configuration

Update configuration file [`config/collectd.conf.template`](../../config/collectd.conf.template), then run

```bash
fab update
```

To collec data into InfluxDB, the following part will be replace automatically to the InfluxDB IP address and port.
```
<Plugin network>
  Server "{influxdb.ip}" "{influxdb.port}"
</Plugin>
```
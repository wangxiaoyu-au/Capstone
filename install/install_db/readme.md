# Install InfluxDB & Grafana

```bash
fab install
```

After installation, there are some manual steps need to be taken.

See http://www.inanzzz.com/index.php/post/ms6c/collectd-influxdb-and-grafana-integration

There are steps can't automated at this moment due to influxdb 1.8 is the stable version
https://docs.influxdata.com/influxdb/v1.8/tools/influx-cli/

InfluxDB 2.0 support commandline query https://v2.docs.influxdata.com/v2.0/reference/cli/influx/query/
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

Then execute 

```bash
fab update
```

If only install InfluxDB

```bash
fab install --grafana=n
```

If only install Grafana

```bash
fab install --influxdb=n
```

# Management

```bash
fab status
fab start
fab stop
```
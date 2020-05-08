
# Install InfluxDB & Grafana

## Installation

```bash
fab install
```

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

## Management

```bash
fab status
fab start
fab stop
```

For `fab status`, when seeing something like

```
...
influxdb  9987  0.1  2.9 1007168 119296 ?      Ssl  May04   8:45 /usr/bin/influxd -config /etc/influxdb/influxdb.conf
...
grafana  23652  0.1  1.1 898868 46508 ?        Ssl  00:10   0:01 /usr/sbin/grafana-server --config=/etc/grafana/grafana.ini --pidfile=/var/run/grafana/grafana-server.pid --packaging=deb cfg:default.paths.logs=/var/log/grafana cfg:default.paths.data=/var/lib/grafana cfg:default.paths.plugins=/var/lib/grafana/plugins cfg:default.paths.provisioning=/etc/grafana/provisioning
```

Means the InfluxDB and Grafana are running correctly.

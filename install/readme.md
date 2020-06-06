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
```

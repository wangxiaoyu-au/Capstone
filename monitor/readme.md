## Monitoring (Need to be updated)

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


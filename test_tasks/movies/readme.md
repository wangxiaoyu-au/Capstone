# Test task data

Download movide data from 

```bash
wget -c --retry-connrefused --tries=0 --timeout=10  http://files.grouplens.org/datasets/movielens/ml-20mx16x32.tar
```

Upload movide data to HDFS

```bash

export $HDFS="hdfs://hdfs_host_ip:90000"
hadoop fs -mkdir -p $HDFS/test_tasks/movies
hadoop fs -put *.csv $HDFS/test_tasks/movies

```
export PYSPARK_PYTHON=python3

hadoop fs -rm -r -f hdfs://192.168.122.247:9000/spark_test/movies-output
spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 4 \
    --maximizeResourceAllocation true\
    --py-files ml_utils.py task2.py \
    --input hdfs://192.168.122.247:9000/spark_test/movies/ \
    --output hdfs://192.168.122.247:9000/spark_test/movies-output/

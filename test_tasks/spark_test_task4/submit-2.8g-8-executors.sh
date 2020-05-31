export PYSPARK_PYTHON=python3

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 4 \
    --executor-memory 1433mb \
    --driver-memory 1433mb \
    --py-files func_utils.py classfication_mp.py \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv

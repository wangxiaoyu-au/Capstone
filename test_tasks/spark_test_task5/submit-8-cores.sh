export PYSPARK_PYTHON=python3

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 4 \
    --executor-cores 1 \
    --total-executor-cores 4 \
    --executor-memory 1400mb \
    --driver-memory 2g \
    --py-files func_utils.py classfication_decision.py \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv

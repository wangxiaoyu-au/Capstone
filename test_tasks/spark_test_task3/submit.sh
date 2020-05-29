export PYSPARK_PYTHON=python3

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 4 \
    --py-files func_utils.py tf_idf.py \
    --executor-memory 2g \
    --driver-memory 2g \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv
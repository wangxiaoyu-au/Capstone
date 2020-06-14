export PYSPARK_PYTHON=python3

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --executor-cores 2 \
    --total-executor-cores 8 \
    --executor-memory 2867mb \
    --conf maximizeResourceAllocation=true \
    --py-files func_utils.py classfication_mp.py \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 3 \
    --py-files task2.py \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv
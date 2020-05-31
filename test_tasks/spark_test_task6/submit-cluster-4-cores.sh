spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode cluster \
    --class ClassifierApp \
    --num-executors 3 \
    --executor-cores 1 \
    --total-executor-cores 4 \
    --executor-memory 1400mb \
    --driver-memory 512mb \
    --class ClassifierApp \
    hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar \
    --input  hdfs://192.168.122.247:9000/spark_test/data/train.tsv

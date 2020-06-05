spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode cluster \
    --class ClassifierApp \
    --executor-cores 2 \
    --total-executor-cores 6 \
    --executor-memory 1800mb \
    --class ClassifierApp \
    hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv \
    --name="test task1"

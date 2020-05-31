hadoop fs -rm -f hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar
hadoop fs -mkdir hdfs://192.168.122.247:9000/spark_test/task6/
hadoop fs -put simple-project_2.11-1.0.jar hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar

spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode cluster \
    --class ClassifierApp \
    --num-executors 4 \
    --executor-cores 8 \
    --executor-memory 2g \
    --driver-memory 2g \
    --class ClassifierApp \
    hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar \
    --input  hdfs://192.168.122.247:9000/spark_test/data/train.tsv

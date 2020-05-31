spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --num-executors 4 \
    --executor-cores 8 \
    --executor-memory 2g \
    --driver-memory 2g \
    --class ClassifierApp \
    ./simple-project_2.11-1.0.jar \
    --input hdfs://192.168.122.247:9000/spark_test/data/train.tsv

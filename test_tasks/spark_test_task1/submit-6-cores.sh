export PYSPARK_PYTHON=python3

hadoop fs -rm -r -f hdfs://192.168.122.247:9000/spark_test/movies-output
spark-submit \
    --master spark://192.168.122.190:7077 \
    --deploy-mode client \
    --executor-cores 2 \
    --total-executor-cores 6 \
    --py-files ml_utils.py AverageRatingPerGenre.py \
    --input hdfs://192.168.122.247:9000/spark_test/movies/ \
    --output hdfs://192.168.122.247:9000/spark_test/movies-output/

hadoop fs -rm -f hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar
hadoop fs -mkdir hdfs://192.168.122.247:9000/spark_test/task6/
hadoop fs -put simple-project_2.11-1.0.jar hdfs://192.168.122.247:9000/spark_test/task6/simple-project_2.11-1.0.jar


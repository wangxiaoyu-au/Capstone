rm -f ../simple-project_2.11-1.0.jar
rm -rf target
rm -rf project
sbt package
cp target/scala-2.11/simple-project_2.11-1.0.jar ../simple-project_2.11-1.0.jar


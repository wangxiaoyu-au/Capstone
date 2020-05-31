import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.feature.Word2Vec
import org.apache.spark.ml.feature.Tokenizer
import org.apache.spark.ml.feature.StopWordsRemover
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.StringIndexer
import org.apache.spark.ml.classification.RandomForestClassifier
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
import org.apache.spark.sql.functions.udf

object ClassifierApp {

    def main(args: Array[String]) {
        val spark = SparkSession.builder.appName("spark session example").getOrCreate()

        val train_datafile = args.collectFirst{case a if a.contains("://") => a}.getOrElse("")
        val train_df = spark.read.
                option("header","true").
                option("sep", "\t").
                csv(train_datafile)

        val train_sents1 = train_df.select("genre", "sentence1")

        val udf_lower = udf { s: String => s.toLowerCase }
        val train_sents1_lower = train_sents1.withColumn("lower_sents", udf_lower(train_sents1("sentence1")) )

        val udf_remove_punctuation = udf { s: String => """[^\w\s]""".r.replaceAllIn(s, "") }
        val train_sents1_rv_punc = train_sents1_lower.withColumn("rv_punc_sents", udf_lower(train_sents1_lower("lower_sents")) )


        val tokenizer = new Tokenizer().setInputCol("rv_punc_sents").setOutputCol("tokens")
        val remover = new StopWordsRemover().setInputCol("tokens").setOutputCol("filtered_tokens")
        val w2v = new Word2Vec().setInputCol("filtered_tokens").setOutputCol("avg_word_embed").setVectorSize(300).setMinCount(0)

        val doc2vec_pipeline = new Pipeline().setStages(Array(tokenizer,remover,w2v))
        val doc2vec_model = doc2vec_pipeline.fit(train_sents1_rv_punc)
        val doc2vecs_df = doc2vec_model.transform(train_sents1_rv_punc)
        val splits = doc2vecs_df.randomSplit(Array(0.8, 0.2))
        val w2v_train_df = splits(0)
        val w2v_test_df = splits(1)
        val genre2label = new StringIndexer().setInputCol("genre").setOutputCol("label")
        val rf_classifier = new RandomForestClassifier().setLabelCol("label").setFeaturesCol("avg_word_embed")

        val rf_classifier_pipeline = new Pipeline().setStages(Array(genre2label,rf_classifier))
        val rf_predictions = rf_classifier_pipeline.fit(w2v_train_df).transform(w2v_test_df)

        val rf_model_evaluator = new MulticlassClassificationEvaluator().setLabelCol("label").setPredictionCol("prediction").setMetricName("accuracy")

        val accuracy = rf_model_evaluator.evaluate(rf_predictions)
        println(s"Learned classification tree model:\n ${accuracy}")
    }
}

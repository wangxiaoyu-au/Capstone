# -*- coding: utf-8 -*-
"""COMP5349_TF-IDF Kmeans Clustering (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hg09bOu1jnXv1_IalCBvNAUhxYW6ecxs

# COMP5349 Assignment Part II-1: 
## TF-IDF based Kmeans Sentence Clustering#
"""

# Import all necessary libraries and setup the environment for matplotlib
from pyspark.sql import SparkSession
from pyspark.ml.feature import PCA
from pyspark.ml.clustering import KMeans
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
import numpy as np
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer, StopWordsRemover
from pyspark.ml.clustering import KMeans, LDA, BisectingKMeans
from func_utils import *

spark = SparkSession \
    .builder \
    .appName("comp5349 sentences clustering") \
    .getOrCreate()

train_datafile = get_args().input
train_df = spark.read.csv(train_datafile,header=True,sep='\t')


# using 1000 records as a small set debugging data
train_sents1 = train_df.select('genre', 'sentence1')
train_sents2 = train_df.select('genre', 'sentence2')
# train_sents1.show(5)


udf_lower = F.udf(lower_folding, StringType() )
train_sents1_lower = train_sents1.withColumn('lower_sents', udf_lower('sentence1') )
# train_sents1_lower.show(5)


udf_rv_punc = F.udf(remove_punctuation_re, StringType() )
train_sents1_rv_punc = train_sents1_lower.withColumn('rv_punc_sents', udf_rv_punc('lower_sents') )

tokenizer = Tokenizer(inputCol="rv_punc_sents", outputCol="tokens")
remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")
hashingTF = HashingTF(inputCol="filtered_tokens", outputCol="rawFeatures", numFeatures=50000)
idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=3)

bkm = BisectingKMeans().setK(5).setSeed(9601).setFeaturesCol("features")

from pyspark.ml import Pipeline
idf_pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, bkm])

idf_model = idf_pipeline.fit(train_sents1_rv_punc)

idf_results = idf_model.transform(train_sents1_rv_punc)
idf_results.cache()

count_idf_res = idf_results.select('genre', 'prediction')\
       .groupBy('genre', 'prediction')\
       .count()\
       .orderBy(['genre', 'count'], ascending=[1, 0])

def genre_to_idx(x):    
    g_2_i = {'fiction': 0, 'government': 2, 'slate': 1, 'telephone': 3, 'travel': 4}
    return g_2_i[x]

udf_g2i = F.udf(genre_to_idx)
idf_results_genre_encoding = idf_results.withColumn('actual', udf_g2i('genre') )
# results_genre_encoding.select('genre','actual').show(5)


idf_pred_list   = idf_results_genre_encoding.select('prediction').rdd.flatMap(lambda x: x).collect()
idf_actual_list = idf_results_genre_encoding.select('actual').rdd.flatMap(lambda x: x).collect()
idf_actual_int_list = [int(i) for i in idf_actual_list]



from sklearn.metrics import confusion_matrix 
idf_conf = confusion_matrix(idf_actual_int_list, idf_pred_list, normalize = 'true') 
idf_conf

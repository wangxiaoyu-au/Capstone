# Calculate the average rating of each genre
# In order to run this, we use spark-submit, below is the 
# spark-submit  \
#   --master local[2] \
    #   AverageRatingPerGenre.py
#   --input input-path
#   --output outputfile

from pyspark import SparkContext
from ml_utils import *
import argparse


if __name__ == "__main__":
    sc = SparkContext(appName="Average Rating per Genre")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="the input path",
                        default='~/comp5349/lab_commons/week5/')
    parser.add_argument("--output", help="the output path", 
                        default='rating_out_script') 
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    ratings = sc.textFile(input_path + "ratings.csv")
    movieData = sc.textFile(input_path + "movies.csv")
    movieRatings = ratings.map(extractRating)
    movieGenre = movieData.flatMap(pairMovieToGenre) # we use flatMap as there are multiple genre per movie
    genreRatings = movieGenre.join(movieRatings).values()
    genreRatingsAverage = genreRatings.aggregateByKey((0.0,0), mergeRating, mergeCombiners, 1).map(mapAverageRating)
    genreRatingsAverage.saveAsTextFile(output_path)

# Yelp-Topic-Modelling
CSC 522 - Providing Business Intelligence to Restaurant Users by Topic Modelling of User Reviews

Constants.py contains the file path to the dataset as well as the constants used in the project.

Corpus.py - After pre-processing all the reviews and using the usefulness > 4 threshold, a corpus of reviews is generated.

Database.py - It contains the insert and update queries for the MongoDB database. 

LDA_train.py - Here we train the corpus data to generate the topics.

Practice.py - It is just for practising the code and writing find queries

Rests_id_Sample.txt - This is a txt file which contains the restaurant IDs for some of the restaurants with the most reviews 

Test_Eval.py - Here we hold out 75%-25% as training-testing data and we perform LDA based topic-modelling on the corpus data. 

UTFToAscii.py - We convert the dictionary from UTF to ASCII to overcome MongoDB and pyMongo limitations.

check.py - This is one of the major outcomes of our project. Restaurant owners can see the various ratings for each of the topic generated and can compare these ratings with the Yelp dataset ratings.

corel_main_rests.py - This file is used to calculate the correlation between various ratings for the major restaurants listed in Rests_id_Sample.txt 

corelation.py - This file is used to calculate the correlation between various ratings for all the restaurants 

filter_noise.py - It helps filter out the words not relevant obtained from the corpus.

predict.py - Any new reviews coming in can be categorised into different topics using this file.

rests.txt - It contains the restaurants ids and the number of reviews each restaurants have.

stopwords.txt - It contains the list of words that need to be filtered out and are not at all relevant to the corpus

topics.txt

topics_15.txt - It extracts the 15 topics 

topics_50.txt - It extracts the 50 topics 

trials.py - It is just for practising the code and writing find queries

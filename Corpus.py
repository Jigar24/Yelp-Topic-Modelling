import json

from pymongo import MongoClient
from Constants import constants

from nltk import WordNetLemmatizer

from nltk.corpus import stopwords
import nltk

corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]

stopset = set(stopwords.words('english'))

lmtzr = WordNetLemmatizer()
review_cursor = reviews_collection.find()
print review_cursor.count()
stopwords = {}
with open('stopwords.txt', 'rU') as f:
    for line in f:
        stopwords[line.strip()] = 1
print stopwords

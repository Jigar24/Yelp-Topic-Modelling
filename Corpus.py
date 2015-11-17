import json

from pymongo import MongoClient
from Constants import constants

from UTFToAscii import convert
from nltk import WordNetLemmatizer

from nltk.corpus import stopwords
import nltk
import nltk.data 
from nltk.tag import pos_tag

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

_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)
db = MongoClient()[constants.DATABASE]
#db.drop_collection(constants.CORPUS_COLLECTION)
print corpus_collection.find().count()

for i in range(review_cursor.count()):
#for i in range(400239,review_cursor.count()):
        
        try :
             review =review_cursor.__getitem__(i)
			 
        except Exception:
             print 'Exceptions..!!!!!!'
             continue
        review_vote = convert(review['votes'])    
        words = []
		
        if review_vote['useful'] > 4 :
		
            print i , " " , review_vote['useful']
            sentences = nltk.sent_tokenize(review["review_text"].lower())
            for sentence in sentences:
                tokens = nltk.word_tokenize(sentence)
                filteredWords = [word for word in tokens if word not in stopwords]
                tagged_text = tagger.tag(filteredWords)

                for word, tag in tagged_text:
                    if tag in ['NN','NNS'] :
                        words.append(lmtzr.lemmatize(word))

            corpus_collection.insert({
                  "_id" : review["_id"],
                  "words": words
            })
		
#print corpus_collection.find().count
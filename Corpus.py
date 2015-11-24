import json
import logging

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

review_cursor = reviews_collection.find()
wnl = WordNetLemmatizer()
print review_cursor.count()

stop_words = convert(stopwords.words('english'))

with open('stopwords.txt', 'rU') as f:
    for line in f:
        stop_words.append(line.strip())
print stop_words

_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'
		
logging.basicConfig(filename='example.log',level=logging.INFO)		
#db = MongoClient()[constants.DATABASE]
#db.drop_collection(constants.CORPUS_COLLECTION)
print corpus_collection.find().count()


for i in range(review_cursor.count()):
        try :
             review =review_cursor.__getitem__(i)
			 
        except Exception:
             print 'Exception'
             continue
        review_vote = convert(review['votes'])    
        words = []
		
        if review_vote['useful'] > 4 :
		
            #print i , " " , review_vote['useful']
            logging.info(i)
            sentences = nltk.sent_tokenize(review["review_text"].lower())
            for sentence in sentences:
                tokens = nltk.word_tokenize(sentence)
                filteredWords = [word for word in tokens if word not in stop_words]
                tagged_text = tagger.tag(filteredWords)

                for word, tag in tagged_text:
                    words.append(wnl.lemmatize(word,get_wordnet_pos(tag)))

            corpus_collection.insert({
						"_id" : review["_id"],
						"words": words,
						"business_id" : review["business_id"],
						"user_id" : review ["user_id"],
						"stars" : review["stars"]
			})



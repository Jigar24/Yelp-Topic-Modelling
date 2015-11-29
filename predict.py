import logging
import json
from pymongo import MongoClient
from Constants import constants
from UTFToAscii import convert
from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

db = MongoClient()[constants.DATABASE]
topic_rating_collection = MongoClient()[constants.DATABASE][constants.TOPIC_RATING_COLLECTION]
restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
review_cursor = reviews_collection.find()
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
cursor = corpus_collection.find()

print topic_rating_collection.find().count()
#db.drop_collection(topic_rating_collection)

#f = open('latent_ratings.txt','w')
class Predict():
    def __init__(self):
        dictionary_path = "Data/Dict"
        lda_model_path = "Data/Online_LDA"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def run(self,i):
		review = cursor.__getitem__(i)
		new_review_bow = self.dictionary.doc2bow(review['words'])
		new_review_lda = self.lda[new_review_bow]
		
		print i
		
		#f.write(i'\t')
		'''topic_rating_collection.update_one({'_id':review['_id']},{"$set":{
		"_id" : review['_id'],
		"business_id" : review['business_id'],
		"user_id" : review ["user_id"],
		"stars" : review["stars"],
		"rating" : new_review_lda
		}})'''
		topic_rating_collection.insert({
		"_id" : review['_id'],
		"business_id" : review['business_id'],
		"user_id" : review ["user_id"],
		"stars" : review["stars"],
		"rating" : new_review_lda
		})
		
		#f.write(str(new_review_lda))
		#f.write('\n')

predict = Predict()
def main():
	#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	for i in range(cursor.count()):
		#corpus_review = cursor.__getitem__(i)
		#print (corpus_review)
		#review_id = reviews_collection.find_one( {'_id': corpus_review['_id'] } )
		#new_review = review_id['review_text']
		#predict = Predict()
		predict.run(i)
		


if __name__ == '__main__':
    main()



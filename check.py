import json
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants

restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
topic_rating_collection = MongoClient()[constants.DATABASE][constants.TOPIC_RATING_COLLECTION]
corpus_cursor = corpus_collection.find()
restaurant_cursor = restaurants_collection.find()
topic_rating_cursor = topic_rating_collection.find()

for i in range(restaurant_cursor.count()):
	try:		
		rest =restaurant_cursor.__getitem__(i)
		print ("aa")
		reviews = corpus_collection.find({'business_id': rest['_id']})
		print ('asdf')
		print (reviews.count())
		for review in reviews:
			print (review['_id'])
			topic_rating = topic_rating_collection.find_one({'_id' : review['_id']})
			print topic_rating
	except Exception:
		print ('Exception')
		continue


		
		
		
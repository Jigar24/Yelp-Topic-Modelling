import json
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants


restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
review_cursor = reviews_collection.find()
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
cursor = corpus_collection.find()

for i in range(10):
	try:
		corpus_review = cursor.__getitem__(i)
		print (corpus_review['_id'])
		print(convert(corpus_review['words']))
		"""review_id = reviews_collection.find_one( {'_id': corpus_review['_id'] } )
		print review_id['review_text']"""
		#for doc in review_id:
		#	print i
		#	print doc
		#print convert(review['review_text'])
	except Exception:
		print 'Exception'
		continue

with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_business.json') as business:
	for line in business:
		business_info = json.loads(line)

val = restaurants_collection.find_one( {"_id" : "SQ0j7bgSTazkVQlF5AnqyQ" })

#print convert(review)

		
		
		
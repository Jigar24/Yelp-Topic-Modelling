import json
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants


restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
corpus_cursor = corpus_collection.find()
restaurant_cursor = restaurants_collection.find()
review_cursor = reviews_collection.find()
#rest = restaurants_collection.find()
#print (reviews_collection.find_one()['_id'])

for i in range(restaurant_cursor.count()):
	try:		
		rest =restaurant_cursor.__getitem__(i)
		print ("aa")
		reviews = corpus_collection.find({'business_id': rest['_id']})
		print ('asdf')
		print (reviews.count())
		#for review in reviews:
			#print (review['_id'])
	except Exception:
		print ('Exception')
		continue



with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_business.json') as business:
	for line in business:
		business_info = json.loads(line)

val = restaurants_collection.find_one( {"_id" : "SQ0j7bgSTazkVQlF5AnqyQ" })

#print convert(review)

		
		
		
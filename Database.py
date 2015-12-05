import json
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants


restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
db = MongoClient()[constants.DATABASE]
db.drop_collection(restaurants_collection)

print restaurants_collection.find().count()

with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_business.json') as business:
	for line in business:
		business_info = json.loads(line)
		
		if "Restaurants" in business_info["categories"] :
			restaurants_collection.insert({
				"_id" : business_info["business_id"],
				"review_count" : business_info["review_count"],
				"name" : business_info["name"],
				"stars" : business_info["stars"],
				"attributes" : business_info["attributes"],
				"categories" : business_info["categories"]
			})
print restaurants_collection.find().count()

#val = restaurants_collection.find_one( {"_id" : "SQ0j7bgSTazkVQlF5AnqyQ" })
#print convert(val)

with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_review.json') as reviews:
	for line in reviews:
		review = json.loads(line)
		
		isRestaurant = restaurants_collection.find({"_id" : review["business_id"]}).count()
		
		if isRestaurant!=0:
			reviews_collection.insert({
				"_id" : review["review_id"],
				"business_id" : review["business_id"],
				"user_id" : review ["user_id"],
				"stars" : review["stars"],
				"votes" : review["votes"],
				"review_date" : review["date"],
				"review_text" : review["text"]
			})
		
		
		
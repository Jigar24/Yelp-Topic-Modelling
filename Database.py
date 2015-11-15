import json, ast
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants


restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]

with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_business.json') as business:
	for line in business:
		business_info = json.loads(line)
		
		if "Restaurants" in business_info["categories"] :
			restaurants_collection.insert({
				"_id" : business_info["business_id"],
				"review_count" : business_info["review_count"],
				"stars" : business_info["stars"],
				"attributes" : business_info["attributes"],
				"categories" : business_info["categories"]
			})



val = restaurants_collection.find_one( {"_id" : "SQ0j7bgSTazkVQlF5AnqyQ" })
		
print convert(val)

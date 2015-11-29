import json
import collections
from UTFToAscii import convert

from pymongo import MongoClient
from Constants import constants

user_collection = MongoClient()[constants.DATABASE][constants.USER_COLLECTION]
#count = 0

with open(constants.JSON_DATASET_FILE+'yelp_academic_dataset_user.json') as user:
	for line in user:
		user_info = json.loads(line)
		user_collection.insert({
			"_id" : user_info["user_id"],
			"name" : user_info["name"],
			"average_stars" : user_info["average_stars"],
			"votes" : user_info["votes"],
			"friends" : user_info["friends"],
			"elite" : user_info["elite"],
			"fans" : user_info["fans"]
			})
		#count=count+1
		#print (count)

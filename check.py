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

#for i in range(93,94):	
rest =restaurant_cursor.__getitem__(93)
reviews = corpus_collection.find({'business_id': rest['_id']})
#print (reviews.count())
#for review in reviews:
	#print review['stars']
topics = []
for i in range(15):
	topic_rate = 0.0
	topic_count = 0
	reviews = corpus_collection.find({'business_id': rest['_id']})
	for review in reviews:
		#print i
		topic_rating = topic_rating_collection.find_one({'_id' : review['_id']})
		val = []
		val = [item for item in topic_rating['rating'] if item[0] == i]
		if val: 
			topic_rate = topic_rate + review['stars']
			topic_count +=1	
	if topic_count > 0:
		topics.append((i,round(topic_rate/topic_count,2), topic_count))
print 'Topic','\t','Rating','\t','Count'
for topic in topics:
		print topic[0],'\t',topic[1],'\t', topic[2] 
	

		
		
		
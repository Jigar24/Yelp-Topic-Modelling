import json
import collections
from UTFToAscii import convert
from scipy.stats.stats import pearsonr   

from pymongo import MongoClient
from Constants import constants

restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
topic_rating_collection = MongoClient()[constants.DATABASE][constants.TOPIC_RATING_COLLECTION]
user_collection = MongoClient()[constants.DATABASE][constants.USER_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
corpus_cursor = corpus_collection.find()
restaurant_cursor = restaurants_collection.find()
topic_rating_cursor = topic_rating_collection.find()
user_cursor = user_collection.find()
'''
f = open('rests.txt','w')

print restaurant_cursor.count()

list = []

for i in range(restaurant_cursor.count()):
	rest =restaurant_cursor.__getitem__(i)
	reviews = corpus_collection.find({'business_id': rest['_id']})
	if reviews.count() > 9:
		print i
		list.append((i,reviews.count()))
		f.write (str(i))
		f.write('\t')
		f.write(str(reviews.count()))
		f.write('\n')

print len(list)
'''	

#for i in range(93,94):	
rest =restaurant_cursor.__getitem__(5227)
reviews = corpus_collection.find({'business_id': rest['_id']})
#print (reviews.count())
#for review in reviews:
	#print review['stars']
#print rest['stars']
print '\n'
print ("Restaurant : %s" % rest['name'])
print '\n'
topics = []
glob_norm = 0.0
glob_fan =  0.0
glob_use = 0.0
glob_count = 0.0 
for i in range(15):
	topic_rate = 0.0
	fan_rate = 0.0
	useful_rate = 0.0
	topic_count = 0
	fan_count = 0
	useful_count = 0
	reviews = corpus_collection.find({'business_id': rest['_id']})
	top =['Game \t', 'Chinese', 'Cafe \t','Japanese','Breakfast','Pizza \t','Dressings','Buffet \t','Diner \t','Drinks \t','Tap \t','Deli \t','Service time','Fast food','Mexican']
	for review in reviews:
		#print i
		topic_rating = topic_rating_collection.find_one({'_id' : review['_id']})
		user = user_collection.find_one({'_id' : topic_rating['user_id']})
		raw_review = reviews_collection.find_one({'_id' : review['_id']})
		
		val = []
		val = [item for item in topic_rating['rating'] if item[0] == i]
		if val: 
			topic_rate = topic_rate + review['stars']
			fan_rate += (user['fans']+1) * review['stars']
			useful_rate += (raw_review['votes']['useful'] + 1) * review['stars']
			topic_count +=1	
			fan_count += (user['fans'] + 1 )
			useful_count += (raw_review['votes']['useful'] + 1)
	if topic_count > 0:
		glob_count += topic_count
		glob_norm += round(topic_rate/topic_count,2) * topic_count
		glob_fan += round(fan_rate/fan_count,2) * topic_count
		glob_use += round(useful_rate/useful_count,2) * topic_count
		topics.append((i,top[i],round(topic_rate/topic_count,2), round(fan_rate/fan_count,2),round(useful_rate/useful_count,2),topic_count))
print 'No.','\t','Topic Name','\t','Rating','\t','FanRat','\t','Useful','\t','Count'
for topic in topics:
		print topic[0],'\t',topic[1],'\t', topic[2], '\t', topic[3], '\t', topic[4],'\t', topic[5]
print '\n'
print 'Yelp Rating %r' % rest['stars']
print 'Fan Rating %r' % round(glob_fan/glob_count,2)
#print 'Correlation %r' % pearsonr(rest['stars'],glob_fan/glob_count)
print 'User Rating %r' % round(glob_norm/glob_count,2)
print 'Usefulness Rating %r' % round(glob_use/glob_count,2)
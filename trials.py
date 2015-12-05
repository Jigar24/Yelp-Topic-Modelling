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
a = [4.5,4.3,5]
b = [3.1,4.3,5]
rest_rating = []
print 'Cor: ' 
pr =  pearsonr(a,b)[0]
pr = round(pr*100,2)
print '%r %%'% pr

print restaurant_cursor.count()
print corpus_collection.count()

for i in range(2):
	print i
	rest =restaurant_cursor.__getitem__(i)
	reviews = corpus_collection.find({'business_id': rest['_id']})
#print (reviews.count())
	#print ("Restaurant : %s" % rest['name'])
	#print ("Restaurant stars: %s" % rest['stars'])
	rest_rating.append(rest['stars'])
print (rest_rating)
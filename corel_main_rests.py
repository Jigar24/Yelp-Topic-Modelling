import json
import collections
from UTFToAscii import convert
from scipy.stats.stats import pearsonr   
#from tp import *
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
fan_rating=[]
useful_rating=[]
user_rating=[]
yelp_rating =[]
fra = []
ura = []
fua = []
fura=[]
rests_list = [5029,5210,5227,7371,14881,14912,17818]
for i in (rests_list):
#for i in range(3):

	print i
	rest =restaurant_cursor.__getitem__(i)
	reviews = corpus_collection.find({'business_id': rest['_id']})
	#print (reviews.count())
	#for review in reviews:
		#print review['stars']
	#print rest['stars']
	#print '\n'
	print ("Restaurant : %s" % rest['name'])
	#print '\n'
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
		top =['Game \t', 'Chinese', 'Cafe \t','Japanese','Breakfast','Pizza \t','Dressings','Diner \t','Buffet \t','Drinks \t','Tap \t','Deli \t','Service time','Fast food','Mexican']
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
	#print 'No.','\t','Topic Name','\t','Rating','\t','FanRat','\t','Useful','\t','Count'
	#for topic in topics:
			#print topic[0],'\t',topic[1],'\t', topic[2], '\t', topic[3], '\t', topic[4],'\t', topic[5]
	#print '\n'
	#print 'Yelp Rating %r' % rest['stars']
	if glob_count ==0:
		glob_count=1
	#print glob_fan
	#print glob_count
	fanr = round(glob_fan/glob_count,2)
	fan_rating.append(fanr)
	#print 'Fan Rating %r' % round(glob_fan/glob_count,2)
	#print 'Correlation %r' % pearsonr(rest['stars'],glob_fan/glob_count)
	usrr = round(glob_norm/glob_count,2)
	user_rating.append(usrr)
	#print 'User Rating %r' % round(glob_norm/glob_count,2)
	usflr = round(glob_use/glob_count,2)
	useful_rating.append(usflr)
	#print 'Usefulness Rating %r' % round(glob_use/glob_count,2)
	yelp_rating.append(rest['stars'])
	fra.append((fanr+usrr)/2)
	ura.append((usrr+usflr)/2)
	fua.append((fanr+usflr)/2)
	fura.append((fanr+usflr+usrr)/3)
	
#print fan_rating
#print user_rating
#print useful_rating
#print yelp_rating
#print fra
#print ura
#print fua
#print fura
print('\n')
sb = 'Correlation between Review Usefulness and User Rating : '
pr2 =  pearsonr(useful_rating,user_rating)[0]
pr2 = round(pr2*100,2)
print '%s %r %%'% (sb,pr2)
print('\n')
sa = 'Correlation between Yelp and Fan Rating : '
pr =  pearsonr(yelp_rating,fan_rating)[0]
pr = round(pr*100,2)
print '%s %r %%'% (sa,pr)
sc = 'Correlation between Yelp and Usefulness Rating : '
pr3 =  pearsonr(yelp_rating,useful_rating)[0]
pr3 = round(pr3*100,2)
print '%s %r %%'% (sc,pr3)
sd = 'Correlation between Yelp and User Review Rating : '
pr4 =  pearsonr(yelp_rating,user_rating)[0]
pr4 = round(pr4*100,2)
print '%s %r %%'% (sd,pr4)
print('\n')
se = 'Correlation between Yelp and Fan+User Review Rating : '
pr5 =  pearsonr(yelp_rating,fra)[0]
pr5 = round(pr5*100,2)
print '%s %r %%'% (se,pr5)
sf = 'Correlation between Yelp and Usefulness+User Review Rating : '
pr6 =  pearsonr(yelp_rating,ura)[0]
pr6 = round(pr6*100,2)
print '%s %r %%'% (sf,pr6)
sg = 'Correlation between Yelp and Usefulness+Fans Rating : '
pr7 =  pearsonr(yelp_rating,fua)[0]
pr7 = round(pr7*100,2)
print '%s %r %%'% (sg,pr7)
print('\n')
sh = 'Correlation between Yelp and Usefulness+Fans+User Rating : '
pr8 =  pearsonr(yelp_rating,fua)[0]
pr8 = round(pr8*100,2)
print '%s %r %%'% (sh,pr8)
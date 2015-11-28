from pymongo import MongoClient
from Constants import constants
from UTFToAscii import convert

filter_words = ['uni','n\'t','marrow',')','umamimi','ale','pa','r.','\'s','eric','des','(','--','mto','je','...','na','gon','1.','2.','3.','4.','5.','6.','-the','ls','de','fois',
'gras','il','mi','blah','..','$','#','pho','http','2','1','3','mama','gordon','la','\xe0','une','du','qui','thing','contender','aji','roughly','le','mais','slider',
'monte','wynn','arepas','\'m',']','--','-','\'ll','\'\'','``','w/','pet','line','kink','groupon','est','make','mom','jalape\xf1os','newly','dad','dans','aria','\'\'','\'ve','tempe','signage','hollywood']

corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
cursor = corpus_collection.find()

for i in range(cursor.count()):
    
	review =cursor.__getitem__(i)
	print i
	#print review
	list = [word for word in review['words'] if word not in filter_words]
	#print cursor
	corpus_collection.update_one({'_id':review['_id']},{"$set":{'words':list,"business_id" : review["business_id"],
							"user_id" : review ["user_id"],
							"stars" : review["stars"]}})
print "done"
#print corpus_collection.find_one()
	



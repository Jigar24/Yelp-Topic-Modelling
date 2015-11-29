from pymongo import MongoClient
from Constants import constants

from gensim import corpora
import nltk
import gensim


Dict_path_train = "Data/Dict_train"
Corpus_path_train = "Data/Corpus_train"
LDA_path_train = "Data/Online_LDA_train"

#Dict_path_test = "Data/Dict_test"
Corpus_path_test = "Data/Corpus_test"
#LDA_path_test = "Data/Online_LDA_test"
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
cursor = corpus_collection.find()


dictionary = corpora.Dictionary(review['words'] for review in cursor)
corpora.Dictionary.save(dictionary,Dict_path_train)

dictionary = corpora.Dictionary.load(Dict_path_train)
#i = 0
bow_train = []
for i in range(0,30000):
    #print i
    review =cursor.__getitem__(i)
    bow_train.append(dictionary.doc2bow(review['words']))
	
corpora.BleiCorpus.serialize(Corpus_path_train,bow_train)

corpus_train = corpora.BleiCorpus(Corpus_path_train)

#LDA = gensim.models.LdaModel(corpus,num_topics = 10,id2word=dictionary)
LDA = gensim.models.LdaModel(corpus_train,num_topics = constants.NUM_TOPICS,id2word=dictionary,iterations=500)
LDA.save(LDA_path_train)
print '_________________________________________________________________________'

bow_test = []
for i in range(30000,40755):
    review =cursor.__getitem__(i)
    bow_test.append(dictionary.doc2bow(review['words']))

corpora.BleiCorpus.serialize(Corpus_path_test,bow_test)

corpus_test = corpora.BleiCorpus(Corpus_path_test)

LDA = gensim.models.LdaModel.load(LDA_path_train)
print 'Hii'
print LDA.bound(corpus_test)
print LDA.log_perplexity(corpus_test)

'''
LDA = gensim.models.LdaModel.load(LDA_path)
i=0

f = open('topics_15.txt','w')
for topic in LDA.show_topics(num_topics=20):
	#print 'Topic',i , '::' , topic
	f.write(str(topic))
	f.write('\n')
	i+=1
#print dictionary
'''
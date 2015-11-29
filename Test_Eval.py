from pymongo import MongoClient
from Constants import constants

from gensim import corpora
import nltk
import gensim


Dict_path = "Data/Dict1"
Corpus_path = "Data/Corpus1"
LDA_path = "Data/Online_LDA1"
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]

cursor = corpus_collection.find()
#print dictionary.len()

dictionary = corpora.Dictionary(review['words'] for review in cursor)
#dictionary.filter_extremes(keep_n=100000)
#dictionary.compactify()
corpora.Dictionary.save(dictionary,Dict_path)

bow = []
i=0
print cursor.count()
cursor = corpus_collection.find()
for i in range(0,35000):
    #print i+1
    review =cursor.__getitem__(i)
    bow.append(dictionary.doc2bow(review['words']))
print len(bow)
corpora.BleiCorpus.serialize(Corpus_path,bow)

corpus = corpora.BleiCorpus(Corpus_path)

LDA = gensim.models.LdaModel(corpus,num_topics = 10,id2word=dictionary)
#LDA = gensim.models.LdaModel(corpus,num_topics = 50,id2word=dictionary,alpha='auto',iterations=500)
LDA.save(LDA_path)
print '_________________________________________________________________________'

bow_t = []
for i in range(35000,40753):
    #print i+1
    review =cursor.__getitem__(i)
    bow_t.append(dictionary.doc2bow(review['words']))
print len(bow_t)

corpora.BleiCorpus.serialize(Corpus_path,bow_t)

corpus = corpora.BleiCorpus(Corpus_path)

LDA = gensim.models.LdaModel.load(LDA_path)
print 'Hii'
print LDA.bound(corpus)
print LDA.log_perplexity(corpus)

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
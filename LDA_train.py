from pymongo import MongoClient
from Constants import constants

from gensim import corpora
import nltk
import gensim


Dict_path = "Data/Dict"
Corpus_path = "Data/Corpus"
LDA_path = "Data/Online_LDA"
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
for review in cursor:
    #print i+1
    bow.append(dictionary.doc2bow(review['words']))
print len(bow)
corpora.BleiCorpus.serialize(Corpus_path,bow)

corpus = corpora.BleiCorpus(Corpus_path)


LDA = gensim.models.LdaModel(corpus,num_topics = 15,id2word=dictionary,iterations = 1000)
LDA.save(LDA_path)

print 'Hii'
print LDA.bound(corpus)


LDA = gensim.models.LdaModel.load(LDA_path)
i=0

f = open('topics_15.txt','w')
for topic in LDA.show_topics(num_topics=15):
	#print 'Topic',i , '::' , topic
	f.write(str(topic))
	f.write('\n')
	i+=1
#print dictionary

import logging
import json
from pymongo import MongoClient
from Constants import constants
from UTFToAscii import convert
from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

restaurants_collection = MongoClient()[constants.DATABASE][constants.BUSINESS_COLLECTION]
reviews_collection = MongoClient()[constants.DATABASE][constants.REVIEWS_COLLECTION]
review_cursor = reviews_collection.find()
corpus_collection = MongoClient()[constants.DATABASE][constants.CORPUS_COLLECTION]
cursor = corpus_collection.find()
f = open('latent_ratings.txt','w')
class Predict():
    def __init__(self):
        dictionary_path = "Data/Dict"
        lda_model_path = "Data/Online_LDA"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open('stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def run(self, new_review , i):
       # nouns = self.extract_lemmatized_nouns(new_review)
		new_review_bow = self.dictionary.doc2bow(cursor.__getitem__(i)['words'])
		new_review_lda = self.lda[new_review_bow]
		
		print new_review_lda
		#f.write(i'\t')
		f.write(str(new_review_lda))
		f.write('\n')


def main():
	#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	for i in range(cursor.count()):
		corpus_review = cursor.__getitem__(i)
		#print (corpus_review['_id'])
		review_id = reviews_collection.find_one( {'_id': corpus_review['_id'] } )
		new_review = review_id['review_text']
		predict = Predict()
		predict.run(new_review, i)
		


if __name__ == '__main__':
    main()



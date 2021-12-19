import csv
import random
import os.path
import sys
import time
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import svm
from sklearn.metrics import classification_report
from nltk.tokenize import TweetTokenizer

class Model:

	class PreprocessingTokenizer(object):
		def __init__(self):
			self.tt = TweetTokenizer(reduce_len=True, preserve_case=True)
		def __call__(self, tweet):
			tokenized_tweet = [t if not t.startswith("http") else "<URLURL>" for t in self.tt.tokenize(tweet) if not all(c in string.punctuation for c in t)]
			return tokenized_tweet

	def __init__(self, filename):
		if not os.path.isfile(f"./Model/Datasets/{filename}"):
			raise Exception(f"Could not find file '{filename}' in the Model/Datasets folder.")
		else:
			self.filename = filename

	def get_pan19_data(self):
		#lists that will store all tweets with the same label (0 or 1/real or bot)
		tweets_bot = list()
		tweets_real = list()

		#read in preprocessed data from csv file from path 
		#note: data file shoulod be in the Model/Datasets directory
		with open(f"./Model/Datasets/{self.filename}", encoding="utf-8") as f:
			reader = csv.reader(f)
			#row[0] contans author id
			#row[1] contains label of 0 or 1
			#row[2] contains string with all the authors tweets
			for row in reader:
				if row[1] == '1':	
					tweets_bot.append(row[2])
				if row[1] == '0':
					tweets_real.append(row[2])

		#to randomize order
		random.shuffle(tweets_bot)
		random.shuffle(tweets_real)
		return tweets_bot, tweets_real

	
	def get_cresci_data(self):
		#lists that will store all tweets with the same label (0 or 1/real or bot)
		tweets_bot = list()
		tweets_real = list()

		accounts_count = 0
		is_sample_run = 'sample' in self.filename
		with open(f"./Model/Datasets/{self.filename}", encoding="utf-8") as f:
			reader = csv.reader(f)
			for row in reader:
				accounts_count += 1
				tweets_bot.append(row[2])
		
		cresci_real_accounts = 3394
		genuine_accounts_file = "./Model/Datasets/genuine_accounts_sample.csv" if is_sample_run else "./Model/Datasets/genuine_accounts.csv"
		with open(genuine_accounts_file, encoding="utf-8") as f:
			# read n random lines from genuine_accounts file, where n is the number of bot accounts 
			random_lines = random.sample(f.readlines(), accounts_count if accounts_count < cresci_real_accounts else cresci_real_accounts)
			for row in csv.reader(random_lines):
				tweets_real.append(row[2])

		#to randomize order
		random.shuffle(tweets_bot)
		random.shuffle(tweets_real)
		return tweets_bot, tweets_real


	def preprocess_train_test(self):
		start_time = time.time()
		tweets_bot, tweets_real = self.get_data()
		training, testing = self.split_data(tweets_bot, tweets_real)

		tokenizer = self.PreprocessingTokenizer()
		#create tfidf vectorizer
		vectorizer = TfidfVectorizer(ngram_range = (1,3), min_df =2, tokenizer=tokenizer)
		#dimensionality reducer 
		svd = TruncatedSVD(n_components=200)
		#model classifier
		svc = svm.SVC(kernel = 'linear', C = 1.0)

		self.train_model(training[0], training[1], vectorizer, svd, svc)
		predictedY = self.test_model(testing[0], vectorizer, svd, svc)
		self.evaluate(predictedY, testing[1])
		end_time = time.time()
		print(f"Running time: {end_time - start_time} seconds")


	def get_data(self):
		if "PAN19-Preprocessed" in self.filename:
			return self.get_pan19_data()
		else:
			return self.get_cresci_data()		


	def split_data(self, tweets_bot, tweets_real):
		#list will contain all data for training/testing
		# data in these lists has format [string of tweets, label] (basicall a list of tuples)
		training = list()
		testing = list()

		#these lists will split the training data into their x and y components
		# x components are the tweets
		# y components are the labels
		# x[i] and y[i] should be the coresponding tweets and label
		trainingX = list()
		trainingY = list()
		testingX = list()
		testingY = list()

		# split 60% of the data to training and remaining 40% to testing as was done in the paper
		# doing it like this ensures that we have same amount of 0 and 1 tweets in each set
		# this assumes that tweets0 and tweets1 are the same size
		for i in range(len(tweets_bot)):
			if i < len(tweets_bot)*0.6:
				training.append([tweets_bot[i], 0])
			else:
				testing.append([tweets_bot[i], 0])

		for i in range(len(tweets_real)):
			if i < len(tweets_real)*0.6:
				training.append([tweets_real[i], 1])
			else:
				testing.append([tweets_real[i], 1])
		#shuffle lists so that the order is randomized
		#if not will have first half of each list all labeled 0 and second half all 1's
		#note that we have the training and test sets made before splitting to x and y components
		# 	so that we can shuffle the order while keeping the x and y components together
		random.shuffle(training)
		random.shuffle(testing)

		#now split our shuffled training and testing sets into X and Y components
		for tweet in training:
			trainingX.append(tweet[0])
			trainingY.append(tweet[1])

		for tweet in testing:
			testingX.append(tweet[0])
			testingY.append(tweet[1])
		
		return (trainingX, trainingY), (testingX, testingY)


	def train_model(self, X, Y, vectorizer, svd, classifier):		
		vectorizedX = vectorizer.fit_transform(X)
		reduced_vectorizedX = svd.fit_transform(vectorizedX)

		classifier.fit(reduced_vectorizedX, Y)

	def test_model(self, X, vectorizer, svd, classifier):
		vectorizedX = vectorizer.transform(X)
		reduced_vectorizedX = svd.transform(vectorizedX)

		predictedY = classifier.predict(reduced_vectorizedX)
		return predictedY

	def evaluate(self, predictedY, actualY):
		i=0
		correct = 0
		total = 0

		for row in predictedY:
			if predictedY[i] == actualY[i]:
				correct = correct + 1
			total = total +1
			i = i+1

		print("correct: ")
		print(correct)
		print("total: ")
		print(total)
		print(classification_report(actualY, predictedY))

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Please enter argument on which dataset you wish to model (python Model/model.py filename.csv)")
		print("The dataset file must be in the Model/Datasets folder")
		quit()

	filename = sys.argv[1]
	model = None
	try:
		model = Model(filename)
	except Exception as e:
		print(e)
		quit()
	
	maxInt = sys.maxsize
	while True:
		# decrease the maxInt value by factor 10 
		# as long as the OverflowError occurs.

		try:
			csv.field_size_limit(maxInt)
			break
		except OverflowError:
			maxInt = int(maxInt/10)
	model.preprocess_train_test()

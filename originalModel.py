from collections import defaultdict
import csv
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


#read in preprocessed data from csv file from path 
#note: data file shoulod be in same directory as this file
reader = csv.reader(open("PAN19-Preprocessed.csv"))

#lists that will store all tweets with the samne label (0 or 1/bot or not bot)
tweets0 = list()
tweets1 = list()

#row[0] contans author id
#row[1] contains label of 0 or 1
#row[2] contains string with all the authors tweets
for row in reader:
	if row[1] == '1':	
		tweets1.append(row[2])
	if row[1] == '0':
		tweets0.append(row[2])

#to randomize order
random.shuffle(tweets0)
random.shuffle(tweets1)

#list will contain all data for training/testing
# data in these lists has format [string of tweets, label] (basicall a list of tuples)
training = list()
testing = list()

#these lists will split the training data into thei x and y components
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
for i in range(len(tweets0)):
	if i < len(tweets0)*0.6:
		training.append([tweets0[i], 0])
	else:
		testing.append([tweets0[i], 0])

for i in range(len(tweets1)):
	if i < len(tweets1)*0.6:
		training.append([tweets1[i], 1])
	else:
		testing.append([tweets1[i], 1])
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


#create tfidf vectorizer
vectorizer = TfidfVectorizer(ngram_range = (1,3), min_df =2)
tfidfMatrix = vectorizer.fit_transform(trainingX)

#reduce dimensionality 
svd = TruncatedSVD(n_components=200)
svdMatrix = svd.fit_transform(tfidfMatrix)


clf = svm.SVC(kernel = 'linear', C = 1.0)
# The above is equivalent to clf = svm.LinearSVC(C = 1.0)
clf.fit(svdMatrix,trainingY)


#test model!

testtfidfMatrix = vectorizer.transform(testingX)
#reduce dimensionality 
testsvdMatrix = svd.transform(testtfidfMatrix)

i=0
correct = 0
total = 0
X = clf.predict(testsvdMatrix)

for row in X:
	if X[i] == testingY[i]:
		correct = correct + 1
	total = total +1
	i = i+1

print("correct: ")
print(correct)
print("total: ")
print(total)



print(classification_report(testingY, X))

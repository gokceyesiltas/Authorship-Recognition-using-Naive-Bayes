#!/usr/bin/python
import os, sys, re
from collections import Counter
from math import log, log10

fileEncoding = "ISO-8859-9"		# for turkish character encoding
functionalWords = []			# functional words 
vocabSize = 0					# the number of unique words in whole training set for BOW training
featuresOfClasses = []			# feature vectors of classes for BOW training
vocabSizeEx = 0					# the number of unique words in whole training set for BOW + extra feature training
featuresOfClassesEx = []		# feature vectors of classes for BOW + extra feature training
trainingDataSize = 0			# number of documents in training set
confusionMatrix = []			# confudion matrix 
classes = []					# class names in training set
truePositiveOfClass = []		# class name - true positive in test set
totalAssignedAsClass = Counter() # class name - the number of assignments to the class in test set
totalTrueClass = []				# class name - the true number of document in the class in test set
recalls = []					# class name - recall values
precisions = []					# class name - precision values


'''
	tokenizes the file according to white spaces.
	deletes punctuation marks.
	returns words in a list
'''
def tokenize(file):
	lines = file.readlines()
	article = " ".join(lines).strip()
	article = article.lower()
	words = article.split()
	wordsWOP = []
	for word in words:
		wordWOP = "".join(re.split('\W', word))
		#if len(wordWOP) > 10:
		#	wordWOP = wordWOP[:10]
		if not wordWOP == '':
			wordsWOP.append(wordWOP)
	return wordsWOP

'''
	takes training path.
	for all directories in training set, looks at all files in the directory. 
	takes tokens by tokenize() function.
	for these words creates a counter which counts the unique words in the list.
	by adding counters, creates a total counter for each directory.
	creates a quadruple for each directory.
	that quadruple contains: class name
							 the number of documents in class
							 the number of words in class
							 unique word - frequency pairs in class
	also calculates the total number of files in whole training set and
					the number of unique words in whole training set.
'''
def trainBOW(trainingPath):
	global vocabSize
	global featuresOfClasses
	global trainingDataSize
	global classes

	directories = []
	for (dirpath, dirnames, filenames) in os.walk(trainingPath):
		directories.extend(dirnames)
		break

	classes = directories

	vocabCounter = Counter()

	# for each directory in the given path 
	for directory in directories:
		newPath = trainingPath + directory + '/'
		files = []
		for (dirpath, dirnames, filenames) in os.walk(newPath):
			files = [i for i in filenames if i.endswith('.txt')]
			break

		length = len(files)
		trainingDataSize += length

		totalCounter = Counter()

		# for each file in the current directory 
		for i in range(0, length):
			filePath = newPath + files[i]
			
			file = open(filePath, encoding=fileEncoding)
			words = tokenize(file)

			occOfWords = Counter(words)
			totalCounter += occOfWords

			file.close()
			
		#print("class:: %s, \t three most common:: %s" %(directory, totalCounter.most_common(3)))

		vocabCounter += totalCounter

		numOfWords = len(list(totalCounter.elements()))

		''' 
			in featuresOfClasses list, there are quadruples which contain
			(class-name, #-of-documents-in-the-class, #-of-words-in-the-class, BOW-of-the-class)
		'''
		featuresOfClasses.append((directory, length, numOfWords, totalCounter))

	vocabSize = len(vocabCounter)

'''
	takes test path, feature quadruples of classes, and vocabulary size.
	for all directories in test set, looks at all files in the directory. 
	takes tokens by tokenize() function.
	for each class, calculates: log(prob(class))
	for each token in training set calculates: log(prob(token|class))
	adds probabilities to find total probability.
	adds class name - probability pair in a list.
	selects class with larger probability value.
	adds true class - (assigned class:how many times) pairs into confusion matrix
'''
def test(testPath, featuresOfClasses, vocabSize):
	global confusionMatrix
	confusionMatrix = []

	directories = []
	for (dirpath, dirnames, filenames) in os.walk(testPath):
		directories.extend(dirnames)
		break

	total = 0

	numOfClasses = len(directories)

	# for each directory in the given path 
	for directory in directories:

		trueVSassigned = Counter()

		newPath = testPath + directory + '/'
		files = []
		for (dirpath, dirnames, filenames) in os.walk(newPath):
			files = [i for i in filenames if i.endswith('.txt')]
			break

		length = len(files)

		total += length

		# for each file in the current directory 
		for i in range(0, length):
			filePath = newPath + files[i]
			
			file = open(filePath, encoding=fileEncoding)
			words = tokenize(file)

			numOfClasses = len(featuresOfClasses)

			probsOfClasses = []

			# for each class in training set
			for j in range(0, numOfClasses):

				probOfClass = 0

				(className, fileSize, numOfWords, classCounter) = featuresOfClasses[j]

				priorProbOfClass = log(fileSize/trainingDataSize)

				probOfDocGivenClass = 0
				for word in words:
					numOfOcc = classCounter[word]
					probOfWordGivenClass = log((numOfOcc+0.006)/(numOfWords+(0.006*vocabSize)))
					probOfDocGivenClass += probOfWordGivenClass
					
				probOfClass = priorProbOfClass + probOfDocGivenClass

				probsOfClasses.append((probOfClass, className))

			# select most probable class
			sortedProbs = sorted(probsOfClasses, reverse=True)
			#print("%s, %s  :::  %s" %(directory, files[i], sortedProbs[0][1]))

			trueVSassigned += Counter([sortedProbs[0][1]])
			
		confusionMatrix.append((directory, trueVSassigned))
				
'''
	looks at confusion matrix.
	for each class counts:  the number of true positive
							the total number of assignments to this class
							the true number of documents in this class
'''
def evaluate():
	global truePositiveOfClass
	global totalAssignedAsClass
	global totalTrueClass

	truePositiveOfClass = []
	totalAssignedAsClass = Counter()
	totalTrueClass = []


	for cla in classes:
		[counter] = [counter for (className, counter) in confusionMatrix if className == cla]
		truePositiveOfClass.append((cla, counter[cla]))
		totalTrueClass.append((cla, sum(counter.values())))
		for key in counter.keys():
			l = [key]*counter[key]
			newCounter = Counter(l)
			totalAssignedAsClass += newCounter

def calculateRecall():
	global recalls 
	recalls = []

	for cla in classes:
		[num] = [num for (claNa, num) in totalTrueClass if claNa == cla]
		[tp] = [tp for (claNa, tp) in truePositiveOfClass if claNa == cla]
		if num == 0:
			recall = 0
		else:
			recall = tp/num
		recalls.append((cla, recall))

def calculatePrecision():
	global precisions
	precisions = []

	for cla in classes:
		[tp] = [tp for (claNa, tp) in truePositiveOfClass if claNa == cla]
		num = totalAssignedAsClass[cla]
		if num == 0:
			precision = 0
		else:
			precision = tp/num
		precisions.append((cla, precision))

def calMacroAvgPre():
	sumPre = 0
	claNum = len(classes)
	for precision in precisions:
		(cla, pre) = precision
		sumPre += pre

	avgPre = sumPre/claNum
	return avgPre

def calMacroAvgRec():
	sumRec = 0
	claNum = len(classes)
	for recall in recalls:
		(cla, rec) = recall
		sumRec += rec

	avgRec = sumRec/claNum
	return avgRec

def calTotTP():
	sumTP = 0
	for cla in classes:
		[tp] = [tp for (claNa, tp) in truePositiveOfClass if claNa == cla]
		sumTP += tp

	return sumTP

def calMicroAvgPre():
	sumTP = calTotTP()
	sumAssigned = 0
	for cla in classes:
		num = totalAssignedAsClass[cla]
		sumAssigned += num

	avgPre = sumTP/sumAssigned
	return avgPre

def calMicroAvgRec():
	sumTP = calTotTP()
	sumTrue = 0
	for cla in classes:
		[num] = [num for (claNa, num) in totalTrueClass if claNa == cla]
		sumTrue += num

	avgRec = sumTP/sumTrue
	return avgRec

def calAvgF(precision, recall):
	return 2*precision*recall/(precision+recall)


'''
	from funtional words text creates a list using tokenize() function
'''
def initializeFunctionalWords():
	functWordPath = "./fwords.txt"
	file = open(functWordPath, encoding=fileEncoding)

	global functionalWords
	functionalWords = tokenize(file)
	file.close()

'''
	takes training path.
	for all directories in training, looks at all files in the directory. 
	takes tokens by tokenize() function.
	for these words creates a counter which counts the unique words in the list.
	by adding counters, creates a total counter for each directory.
	** then deletes functional words from the counter. (difference from trainingBOW() function)
	creates a quadruple for each directory.
	that quadruple contains: class name
							 the number of documents in class
							 the number of words in class
							 unique word - frequency pairs in class
	also calculates the total number of files in whole training set and
					the number of unique words in whole training set.
'''
def trainBOWextra(trainingPath):
	initializeFunctionalWords()
	global vocabSizeEx
	global featuresOfClassesEx

	vocabCounter = Counter()

	directories = []
	for (dirpath, dirnames, filenames) in os.walk(trainingPath):
		directories.extend(dirnames)
		break

	# for each directory in the given path 
	for directory in directories:
		newPath = trainingPath + directory + '/'
		files = []
		for (dirpath, dirnames, filenames) in os.walk(newPath):
			files = [i for i in filenames if i.endswith('.txt')]
			break

		length = len(files)

		totalCounter = Counter()

		# for each file in the current directory 
		for i in range(0, length):
			filePath = newPath + files[i]
			
			file = open(filePath, encoding=fileEncoding)
			words = tokenize(file)

			occOfWords = Counter(words)
			totalCounter += occOfWords

			file.close()

		# remove functional words
		for functionalWord in functionalWords:
			del totalCounter[functionalWord]

		#print("class:: %s, \t three most common:: %s" %(directory, totalCounter.most_common(3)))
			
		vocabCounter += totalCounter

		numOfWords = len(list(totalCounter.elements()))

		''' 
			in featuresOfClasses list, there are quadruples which contain
			(class-name, #-of-documents-in-the-class, #-of-words-in-the-class, BOW-of-the-class)
		'''
		featuresOfClassesEx.append((directory, length, numOfWords, totalCounter))

	vocabSizeEx = len(vocabCounter)
		
if __name__ == '__main__':
	trainingPath = sys.argv[1]
	testPath = sys.argv[2]

	'''
		BOW
	'''
	trainBOW(trainingPath)
	test(testPath, featuresOfClasses, vocabSize)
	evaluate()
	calculateRecall()
	calculatePrecision()

	macroAvgPrecision = calMacroAvgPre()
	macroAvgRecall = calMacroAvgRec()
	macroAvgF = calAvgF(macroAvgPrecision, macroAvgRecall)

	microAvgPrecision = calMicroAvgPre()
	microAvgRecall = calMicroAvgRec()
	microAvgF = calAvgF(microAvgPrecision, microAvgRecall)
	print("Performance Evaluation of BOW")
	print("Micro Averaged Precision:\t%s" %microAvgPrecision)
	print("Micro Averaged Recall:\t%s" %microAvgRecall)
	print("Micro Averaged F value:\t%s" %microAvgF)
	print("Macro Averaged Precision:\t%s" %macroAvgPrecision)
	print("Macro Averaged Recall:\t%s" %macroAvgRecall)
	print("Macro Averaged F value:\t%s" %macroAvgF)


	'''
		BOW without functional words
	'''
	trainBOWextra(trainingPath)
	test(testPath, featuresOfClassesEx, vocabSizeEx)
	evaluate()
	calculateRecall()
	calculatePrecision()

	macroAvgPrecision = calMacroAvgPre()
	macroAvgRecall = calMacroAvgRec()
	macroAvgF = calAvgF(macroAvgPrecision, macroAvgRecall)

	microAvgPrecision = calMicroAvgPre()
	microAvgRecall = calMicroAvgRec()
	microAvgF = calAvgF(microAvgPrecision, microAvgRecall)
	print("\nPerformance Evaluation of BOW + Extra Feature")
	print("Micro Averaged Precision :\t%s" %microAvgPrecision)
	print("Micro Averaged Recall :\t%s" %microAvgRecall)
	print("Micro Averaged F value :\t%s" %microAvgF)
	print("Macro Averaged Precision :\t%s" %macroAvgPrecision)
	print("Macro Averaged Recall :\t%s" %macroAvgRecall)
	print("Macro Averaged F value :\t%s" %macroAvgF)
	

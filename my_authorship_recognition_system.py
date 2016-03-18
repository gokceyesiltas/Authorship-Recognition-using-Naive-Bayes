#!/usr/bin/python
import os, sys, re
from collections import Counter
from math import log, log10

fileEncoding = "ISO-8859-9"
functionalWords = []
vocabSize = 0
featuresOfClasses = []
vocabSizeEx = 0
featuresOfClassesEx = []
trainingDataSize = 0
confusionMatrix = []
classes = []
truePositiveOfClass = []
totalAssignedAsClass = Counter()
totalTrueClass = []
recalls = []
precisions = []

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

		uniqWordsNum = len(totalCounter)
		vocabSize += uniqWordsNum

		numOfWords = len(list(totalCounter.elements()))

		''' 
			in featuresOfClasses list, there are quadruples which contain
			(class-name, #-of-documents-in-the-class, #-of-words-in-the-class, BOW-of-the-class)
		'''
		featuresOfClasses.append((directory, length, numOfWords, totalCounter))

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


def initializeFunctionalWords():
	functWordPath = "./fwords.txt"
	file = open(functWordPath, encoding=fileEncoding)

	global functionalWords
	functionalWords = tokenize(file)
	file.close()

def trainBOWextra(trainingPath):
	initializeFunctionalWords()
	global vocabSizeEx
	global featuresOfClassesEx

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

		print("class:: %s, \t three most common:: %s" %(directory, totalCounter.most_common(3)))
			
		uniqWordsNum = len(totalCounter)
		vocabSizeEx += uniqWordsNum

		numOfWords = len(list(totalCounter.elements()))

		''' 
			in featuresOfClasses list, there are quadruples which contain
			(class-name, #-of-documents-in-the-class, #-of-words-in-the-class, BOW-of-the-class)
		'''
		featuresOfClassesEx.append((directory, length, numOfWords, totalCounter))

		
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
		BOW with extra feature
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


'''
	trainBOW(trainingPath)
	test(testPath)

	evaluate()
	calculateRecall()
	calculatePrecision()

	macroAvgPrecision = calMacroAvgPre()
	macroAvgRecall = calMacroAvgRec()
	macroAvgF = calAvgF(macroAvgPrecision, macroAvgRecall)

	microAvgPrecision = calMicroAvgPre()
	microAvgRecall = calMicroAvgRec()
	microAvgF = calAvgF(microAvgPrecision, microAvgRecall)
'''
	




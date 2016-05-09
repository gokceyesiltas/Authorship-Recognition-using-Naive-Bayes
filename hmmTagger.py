#!/usr/bin/python
import sys, os
import trainHmmTagger

global trainingFile
global testFile
global outputFile

cpostags = ['START', 'Punc', 'Verb', 'Num', 'Adv', 'Dup', 'Conj', 'Ques', 'Postp', 'Interj', 'Noun', 'Pron', 'Det', 'Adj']
cpostagNum = 13


postags = ['START', 'Conj', 'Pron', 'APresPart', 'Num', 'Ord', 'PersP', 'Card', 'NPastPart', 'NInf', 'Dup', 'QuesP', 'Real', 'Zero', 'Range', 'Adv', 'Det', 'Adj', 'AFutPart', 'Postp', 'Interj', 'Verb', 'ReflexP', 'Prop', 'NFutPart', 'Punc', 'Ques', 'APastPart', 'Distrib', 'Noun', 'DemonsP', 'Percent', 'Ratio', 'Time', 'QuantP']
postagNum = 34

global tags
global tagCounter

def transition(prevTag, currentTag):	
	tagPair = "-".join((prevTag, currentTag))
	count = trainHmmTagger.tagTransitionCounter[tagPair]

	#print(tagPair)
	#print(count)

	allTransitions = 0 
	for tag in tags: 
		temp = "-".join((prevTag, tag))
		trans = trainHmmTagger.tagTransitionCounter[temp]
		allTransitions += trans

	if allTransitions != 0:
		prob = count / allTransitions
	else:
		prob = 0
	#print("transition prob %s %s %s" %(prevTag, currentTag, prob))
	return prob


def emission(currentWord, currentTag):
	wordTagPair = "-".join((currentWord, currentTag))
	count = trainHmmTagger.wordTagCounter[wordTagPair]

	#print(wordTagPair)
	#print(count)

	allEmissions = 0
	for tag in tags:
		temp = "-".join((currentWord, tag))
		emis = trainHmmTagger.wordTagCounter[temp]
		allEmissions += emis
	if allEmissions != 0:
		prob = count / allEmissions
	else:
		prob = 0
	#print("emission prob %s %s %s" %(currentWord, currentTag, prob))
	return prob


# sentence is a list of words including START and END 
def viterbi(sentence):
	#print(sentence)
	length = len(sentence)
	V = []
	backPointers = []

	V.append({})
	backPointers.append({})

	for tag in tags:
		V[0][tag] = 0

	V[0]['START'] = 1
	backPointers[0]['START'] = 0

	for step in range(1, length-1):
		#print("################\nstep %s" %step)
		#print(sentence[step])
		V.append({})
		backPointers.append({})
		for currentTag in tags:
			#print("current tag:::::::::: %s" %currentTag)
			maxProb = 0
			backPointer = ""
			emissionProb = emission(sentence[step], currentTag)
			if emissionProb != 0:
				for prevTag in tags:
					transitionProb = transition(prevTag, currentTag)
					prob = V[step-1][prevTag]*transitionProb*emissionProb
					if maxProb < prob:
						maxProb = prob
						backPointer = prevTag
				
			#print(maxProb)
			#print(backPointer)
			V[step][currentTag] = maxProb
			backPointers[step][currentTag] = backPointer

		pr = []
		for tag in tags:
			pr.append(V[step][tag])

		if max(pr) == 0:
			mostCommon = tagCounter.most_common(1)
			#print(mostCommon[0])
			prob = (mostCommon[0][1] / len(list(tagCounter.elements())))
			#print(prob)
			currentTag = mostCommon[0][0]
			(maxProb, backPointer) = max((V[step-1][prevTag] * transition(prevTag, currentTag) * prob, prevTag) for prevTag in tags)
			V[step][currentTag] = maxProb
			backPointers[step][currentTag] = backPointer

		
	V.append({})
	backPointers.append({})

	(prob, backPointer) = max((V[length-2][prevTag], prevTag) for prevTag in tags)
	V[length-1][0] = prob
	backPointers[length-1][0] = backPointer

	#print(V)
	#print(backPointers)

	prev = backPointer
	path = [prev]
	for i in range(1, length-1):
		#print(length-1-i)
		#print(prev)
		prev = backPointers[length-1-i][prev]
		path.append(prev)

	path = list(reversed(path))

	#print("path %s" %path)
	return path


def writeFile(output, sentence, path):
	for i in range(1, len(sentence)-1):
		output.write("%s|%s\n" %(sentence[i], path[i]))
	output.write("\n")


def findTAGS():
	dirName = os.path.dirname(outputFile)
	if not os.path.exists(dirName):
		os.makedirs(dirName)

	output = open(outputFile, 'w+')

	file = open(testFile, encoding="utf-8")
	lines = file.readlines()

	sentence = ['START']
	for line in lines:
		sLine = "".join(line)
		#sLine = sLine.lower()
		fields = sLine.split()
		
		if len(fields) != 0:
			form = fields[1]
			if form != "_":
				sentence.append(form)
				if form == ".":
					sentence.append('END')
		else:
			path = viterbi(sentence)
			writeFile(output, sentence, path)
			#print(sentence)
			sentence = ['START']

	output.close()



if __name__ == '__main__':
	global trainingFile
	global testFile
	global outputFile
	global tags
	global tagCounter
	trainingFile = sys.argv[1]
	testFile = sys.argv[3]
	outputFile = sys.argv[4]
	#if not os.path.exists(outputFile):
	#	os.makedirs(outputFile)

	#goldFile = sys.argv[5]
	if "--cpostag" in sys.argv:
		trainHmmTagger.trainCPOS(trainingFile)
		tags = cpostags
		#print(tags)
		tagCounter = trainHmmTagger.cpostags
	elif "--postag" in sys.argv:
		trainHmmTagger.trainPOS(trainingFile)
		tags = postags
		#print(tags)
		tagCounter = trainHmmTagger.postags
		#print(tagCounter)

	findTAGS()

	
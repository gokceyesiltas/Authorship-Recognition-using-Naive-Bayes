#!/usr/bin/python
import sys

cpostags = ['Punc', 'Verb', 'Num', 'Adv', 'Dup', 'Conj', 'Ques', 'Postp', 'Interj', 'Noun', 'Pron', 'Det', 'Adj']
cpostagNum = 13


postags = ['Conj', 'Pron', 'APresPart', 'Num', 'Ord', 'PersP', 'Card', 'NPastPart', 'NInf', 'Dup', 'QuesP', 'Real', 'Zero', 'Range', 'Adv', 'Det', 'Adj', 'AFutPart', 'Postp', 'Interj', 'Verb', 'ReflexP', 'Prop', 'NFutPart', 'Punc', 'Ques', 'APastPart', 'Distrib', 'Noun', 'DemonsP', 'Percent', 'Ratio', 'Time', 'QuantP']
postagNum = 34

def evaluateCPOS(outputFile, goldFile):
	output = open(outputFile, encoding="utf-8")
	gold = open(goldFile, encoding="utf-8")

	outputLines = output.readlines()
	goldLines = gold.readlines()

	outputTags = []
	goldTags = []

	confusion = {}
	trueTag = {}
	errorRate = {}
	truePos = 0

	for cpostag in cpostags:
		confusion[cpostag] = {}
		errorRate[cpostag] = {}
		trueTag[cpostag] = 0
		for cpostag2 in cpostags:
			confusion[cpostag][cpostag2] = 0
			errorRate[cpostag][cpostag2] = 0

	for goldLine in goldLines:
		sLine = "".join(goldLine)
		#sLine = sLine.lower()
		fields = sLine.split()

		if len(fields) != 0:
			form = fields[1]
			cpostag = fields[3]
			if form != "_":
				goldTags.append(cpostag)

	for outputLine in outputLines:
		sLine = "".join(outputLine).strip()
		splitted = sLine.split("|")
		if len(splitted) == 2:
			tag = splitted[1]
			outputTags.append(tag)

	total = len(outputTags)		

	for i in range(0, total):
		oT = outputTags[i]
		gT = goldTags[i]
		if oT == gT:
			truePos += 1
			confusion[gT][oT] += 1
		else:
			confusion[gT][oT] += 1
		trueTag[gT] += 1

	accuracy = truePos / total
	print("Tag accuracy: %s" %accuracy)

	for tag1 in cpostags:
		for tag2 in cpostags:
			if trueTag[tag1] != 0:
				errorRate[tag1][tag2] = confusion[tag1][tag2] * 100 / trueTag[tag1]
			else:
				errorRate[tag1][tag2] = 0

	#print(errorRate)

	results = open("results.txt", "w+")
	results.write("\t")

	for cpostag in cpostags:
		results.write("%s\t" %cpostag)

	results.write("\n")

	for cpostag1 in cpostags:
		results.write("%s\t" %cpostag1)
		for cpostag2 in cpostags:
			results.write("%s\t" %errorRate[cpostag1][cpostag2])
		results.write("\n")


def evaluatePOS(outputFile, goldFile):
	output = open(outputFile, encoding="utf-8")
	gold = open(goldFile, encoding="utf-8")

	outputLines = output.readlines()
	goldLines = gold.readlines()

	outputTags = []
	goldTags = []

	confusion = {}
	trueTag = {}
	errorRate = {}
	truePos = 0

	for postag in postags:
		confusion[postag] = {}
		errorRate[postag] = {}
		trueTag[postag] = 0
		for postag2 in postags:
			confusion[postag][postag2] = 0
			errorRate[postag][postag2] = 0

	for goldLine in goldLines:
		sLine = "".join(goldLine)
		#sLine = sLine.lower()
		fields = sLine.split()

		if len(fields) != 0:
			form = fields[1]
			postag = fields[4]
			if form != "_":
				goldTags.append(postag)

	for outputLine in outputLines:
		sLine = "".join(outputLine).strip()
		splitted = sLine.split("|")
		if len(splitted) == 2:
			tag = splitted[1]
			outputTags.append(tag)

	total = len(outputTags)		

	for i in range(0, total):
		oT = outputTags[i]
		gT = goldTags[i]
		if oT == gT:
			truePos += 1
			confusion[gT][oT] += 1
		else:
			confusion[gT][oT] += 1
		trueTag[gT] += 1

	accuracy = truePos / total
	print("Tag accuracy: %s" %accuracy)

	for tag1 in postags:
		for tag2 in postags:
			if trueTag[tag1] != 0:
				errorRate[tag1][tag2] = confusion[tag1][tag2] * 100 / trueTag[tag1]
			else:
				errorRate[tag1][tag2] = 0

	#print(errorRate)

	results = open("results.txt", "w+")
	results.write("\t")

	for postag in postags:
		results.write("%s\t" %postag)

	results.write("\n")

	for postag1 in postags:
		results.write("%s\t" %postag1)
		for postag2 in postags:
			results.write("%s\t" %errorRate[postag1][postag2])
		results.write("\n")





if __name__ == '__main__':
	outputFile = sys.argv[1]
	goldFile = sys.argv[2]
	if "--cpostag" in sys.argv:
		evaluateCPOS(outputFile, goldFile)
	elif "--postag" in sys.argv:
		evaluatePOS(outputFile, goldFile)
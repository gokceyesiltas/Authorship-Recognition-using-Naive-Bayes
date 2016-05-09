#!/usr/bin/python
import sys
from collections import Counter

wordTagCounter = Counter()
tagTransitionCounter = Counter()
wordTagList = []
tagTransitionList = []
cpostags = []
postags = []
fileEncoding = "utf-8"

def trainCPOS(fileName):
	wordTagList = []
	tagTransitionList = []
	global wordTagCounter
	global tagTransitionCounter
	global cpostags
	file = open(fileName, encoding=fileEncoding)
	lines = file.readlines()
	previous = "START"
	for line in lines:
		sLine = "".join(line)
		#sLine = sLine.lower()
		fields = sLine.split()

		if len(fields) != 0:
			form = fields[1]
			cpostag = fields[3]
			if form != "_":
				wordTag = "-".join((form, cpostag))
				wordTagList.append(wordTag)
				tagTransition = "-".join((previous, cpostag))
				tagTransitionList.append(tagTransition)
				cpostags.append(cpostag)
				if form == ".":
					tagTransition = "-".join((cpostag, "END"))
					tagTransitionList.append(tagTransition)
				previous = cpostag
				#print(tagTransition)

		else:
			previous = "START"

	wordTagCounter = Counter(wordTagList)			
	tagTransitionCounter = Counter(tagTransitionList)
	cpostags = Counter(cpostags)
	

def trainPOS(fileName):
	wordTagList = []
	tagTransitionList = []
	global wordTagCounter
	global tagTransitionCounter
	global postags
	file = open(fileName, encoding=fileEncoding)
	lines = file.readlines()
	previous = "START"
	for line in lines:
		sLine = "".join(line)
		#sLine = sLine.lower()
		fields = sLine.split()
		
		if len(fields) != 0:
			form = fields[1]
			postag = fields[4]
			if form != "_":
				wordTag = "-".join((form, postag))
				wordTagList.append(wordTag)
				tagTransition = "-".join((previous, postag))
				tagTransitionList.append(tagTransition)
				postags.append(postag)
				if form == ".":
					tagTransition = "-".join((postag, "END"))
					tagTransitionList.append(tagTransition)
				previous = postag
				#print(tagTransition)
		else:
			previous = "START"

	wordTagCounter = Counter(wordTagList)			
	tagTransitionCounter = Counter(tagTransitionList)
	postags = Counter(postags)
	

if __name__ == '__main__':
	fileName = sys.argv[1]
	if "--cpostag" in sys.argv:
		trainCPOS(fileName)
	elif "--postag" in sys.argv:
		trainPOS(fileName)
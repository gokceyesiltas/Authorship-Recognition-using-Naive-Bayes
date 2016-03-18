#!/usr/bin/python
import os, os.path, sys, shutil

dataPath = sys.argv[1]
trainingPath = sys.argv[2]
testPath = sys.argv[3]

directories = []
for (dirpath, dirnames, filenames) in os.walk(dataPath):
	directories.extend(dirnames)
	break

if not os.path.exists(trainingPath):
	os.makedirs(trainingPath)

if not os.path.exists(testPath):
	os.makedirs(testPath)

for directory in directories:
	newPath = dataPath + directory + '/'
	files = []
	for (dirpath, dirnames, filenames) in os.walk(newPath):
		files = [i for i in filenames if i.endswith('.txt')]
		break

	length = len(files)
	trainingSize = int(length * 0.6)

	for i in range(0, trainingSize):
		filePath = newPath + files[i]
		fileTrainingPath = trainingPath + directory + '/' 
		if not os.path.exists(fileTrainingPath):
			os.makedirs(fileTrainingPath)
		shutil.copy(filePath, fileTrainingPath)

	for i in range(trainingSize, length):
		filePath = newPath + files[i]
		fileTestPath = testPath + directory + '/' 
		if not os.path.exists(fileTestPath):
			os.makedirs(fileTestPath)
		shutil.copy(filePath, fileTestPath)

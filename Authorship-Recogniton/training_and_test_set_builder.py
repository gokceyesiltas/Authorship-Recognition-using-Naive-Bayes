#!/usr/bin/python
import os, os.path, sys, shutil

# takes data set path, training data path and test data path
dataPath = sys.argv[1]
trainingPath = sys.argv[2]
testPath = sys.argv[3]

# finds directories in the data set path 
directories = []
for (dirpath, dirnames, filenames) in os.walk(dataPath):
	directories.extend(dirnames)
	break

# if training path doesnt exist, creates the directory
if not os.path.exists(trainingPath):
	os.makedirs(trainingPath)

# if test path doesnt exist, creates the directory
if not os.path.exists(testPath):
	os.makedirs(testPath)

# for all directories in the path 
for directory in directories:
	newPath = os.path.join(dataPath, directory)

	# finds files in the current directory
	files = []
	for (dirpath, dirnames, filenames) in os.walk(newPath):
		files = [i for i in filenames if i.endswith('.txt')]
		break

	# number of files 
	length = len(files)

	# calculates training data size 
	trainingSize = int(length * 0.6)
	#print(directory, length, trainingSize, (length-trainingSize))

	# copies training files into training data path
	for i in range(0, trainingSize):
		filePath = newPath + files[i]
		fileTrainingPath = os.path.join(trainingPath, directory) 
		if not os.path.exists(fileTrainingPath):
			os.makedirs(fileTrainingPath)
		shutil.copy(filePath, fileTrainingPath)

	# copies test files into test data path
	for i in range(trainingSize, length):
		filePath = newPath + files[i]
		fileTestPath = os.path.join(testPath, directory)
		if not os.path.exists(fileTestPath):
			os.makedirs(fileTestPath)
		shutil.copy(filePath, fileTestPath)

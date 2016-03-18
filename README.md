# Authorship Recognition using Naive Bayes
Authorship Recognition using Naive Bayes in Turkish

## Preprocessing Script
This script takes three arguments. First of them is the path of the data set. This path should contain folders with name of authors. In the folders, there should be txt documents of the author. Second and third arguments are path to training data set and test data set which are filled by this program. Program copies 60% of the documents in each folder into training folder by preserving author folders. And program copies remaining 40% of the documents in each folder into training folder by preserving author folders.   
    
To run the program, write the following command from the same folder of the script:   
    
    `python training_and_test_set_builder.py  /path/to/dataset /path/to/training/set /path/to/test/set`    
     
## Recognition and Performance Evaluation Script
This scripts takes two arguments. First of them is the path of training data set. The other is the path of test set. 

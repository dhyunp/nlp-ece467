#NLP Project 2: HMM POS Tagger Confusion Matrix generation by Donghyun Park & Junbum Kim
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import pandas as pd

def confuse(dir):
    tags = []
    doc = open(dir, 'r')
    for line in doc:
        line = line.strip()
        tokens = line.split(" ")
        for token in tokens:
            tag = token.split("/")
            if len(tag) > 1:
                posTag = tag[1]
                tags.append(posTag)
    return tags

def main():
    '''
    print("Enter Predicted Labels File: ", end="")
    predicts = input()
    predictfiles = open("test.list", 'r')
    predictFile = open(predicts, 'r')

    print("Enter True Labels File: ", end="")
    truths = input()
    truthfiles = open("test.labels", 'r')
    truthFile = open(truths, 'r')
    '''

    predictTags = []
    trueTags = []

    dir = input("Enter demo directory: ")
    filename = input("Enter test filename: ")

    demoDir = dir + "/" + filename
    testDir = "test_label/" + filename

    predictTags = confuse(demoDir)
    trueTags = confuse(testDir)

    sum = 0.0
    diag = 0.0
    conf = confusion_matrix(trueTags, predictTags)

    i = 0
    for row in conf:
        j = 0
        print(" ")
        for col in row:
            sum += col
            if i == j:
                diag += col
            j += 1
            print(str(col)+ " ", end="")
        i+=1
        print("\n")

    print("accuracy = " + str(diag/sum) + "\n")
    print("count = " + str(sum) + "\n")
    print("used = " + str(min(len(trueTags), len(predictTags))) + "\n")
    #print(pd.crosstab(trueTags, predictTags, rownames=['True'], colnames=['Predicted'], margins=True))
    print(classification_report(trueTags, predictTags))
    #confPD = pd.DataFrame(conf)
    #confPD.to_excel("outputFile.xlsx", index=False)
    #print(np.array2string(confusion_matrix(trueTags, predictTags)))

if __name__ == "__main__":
    main()

'''
logical progression:
import two files, one true, one predict
parse each line
tokenize the line
take in the tags
do conf matrix
'''

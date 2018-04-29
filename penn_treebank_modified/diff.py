import itertools

checkFolder = raw_input("Insert the name of the folder you want to check: ")
trueFolder = 'test_label'

test_set = open("test.list", "r")
output = open("diffFile", "w")

for document in test_set:
    document = document.strip()
    checkDoc = open(checkFolder + "/" + document, "r")
    trueDoc = open(trueFolder + "/" + document, "r")
    lineNum = 1

    for cLine, tLine in itertools.izip_longest(checkDoc, trueDoc):
        cTokens = cLine.strip().split(" ")
        tTokens = tLine.strip().split(" ")

        if len(cTokens) > len(tTokens):
            output.write("File: " + document + " Line: " + str(lineNum) + " - ERROR: Length of checking file is longer than test label file by " + str(len(cTokens) - len(tTokens)) + " word/s!\n")
        if len(cTokens) < len(tTokens):
            output.write("File: " + document + " Line: " + str(lineNum) + " - ERROR: Length of checking file is shorter than test label file by" + str(len(tTokens) - len(cTokens)) + " word/s!\n")

        for cToken, tToken in itertools.izip_longest(cTokens, tTokens):
            if (cToken is not None) and (tToken is not None):
                cWord = cToken.split("/")
                tWord = tToken.split("/")
                if cWord[0] == tWord[0]:
                    continue
                else:
                    output.write("File: " + document + " Line: " + str(lineNum) +" - ")
                    output.write(cWord[0] + ", " + tWord[0] + "\n")

        lineNum += 1

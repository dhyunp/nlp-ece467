from nltk import sent_tokenize
folder = "train_set"

train_set = open("train.list", "r")
for document in train_set:
	origin = open(folder + "_noline/" + document.strip(), "r")
	train_document = open(folder + "/"+ document.strip(), "w")
	for line in origin:
		sentence = sent_tokenize(line)
		for s in sentence:
			train_document.write(s + "\n")
	train_document.close()
	origin.close()

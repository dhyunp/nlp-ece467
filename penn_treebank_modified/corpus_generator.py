import re
tagset = ['PRP$', 'VBG', 'VBD', '``', 'VBN', 'POS', "''", 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', 'RP', '$', 'NN', '<s>', ',', '.', 'TO', 'PRP', 'RB', ':', 'NNS', 'NNP', 'VB', 'WRB', 'CC', 'PDT', 'RBS', 'RBR', 'CD', 'IN', 'MD', 'NNPS', 'JJS', 'JJR', 'OTH']

train_set = open("test.list", "r")
for document in train_set:
	print "open:", document.strip()
	train_document = open("test_label/" + document.strip(), "r")
	result = open("test_set/" + document.strip(), "w")
	for line in train_document:
		tmp = line.strip().split(' ')
		text = ""
		for token in tmp:
			word = token.split("/")
			text = text + word[0] + " "
		result.write(text + "\n")
		
	result.close()
	train_document.close()
train_set.close()
import random

corpus = "penn_treebank.list"
document = open(corpus, "r")
test_list = "test.list"
train_list = "train.list"
test_result = "test.labels"

train_document = open(train_list, "w")
test_document = open(test_list, "w")
test_result = open(test_result, "w")

for line in document:
	param = line.rstrip()
	file_name = param
	i = random.randint(1,4)
	if i == 1:
		test_document.write(file_name + "\n")
		test_result.write(line)
	else:
		train_document.write(line)

train_document.close()
test_document.close()
test_result.close()
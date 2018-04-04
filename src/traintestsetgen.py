import random

corpus = "list_of_documents"
document = open(corpus, "r")
test_list = corpus + "_test.list"
train_list = corpus + "_train.list"
test_result = corpus + "_test.labels"

train_document = open(train_list, "w")
test_document = open(test_list, "w")
test_result = open(test_result, "w")

for line in document:
	param = line.rstrip().split(" ")
	file_name, tag = param
	i = random.randint(1,3)
	if i == 1:
		test_document.write(file_name + "\n")
		test_result.write(line)
	else:
		train_document.write(line)

train_document.close()
test_document.close()
test_result.close()
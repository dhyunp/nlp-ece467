from shutil import copyfile

corpus = "train.list"
document = open(corpus, "r")
src = "original_tagged_corpus"
dst = "train_set"

for file in document:
	tmp = file.rstrip()
	copyfile(src+"/"+tmp, dst+"/"+tmp)
	
document.close()
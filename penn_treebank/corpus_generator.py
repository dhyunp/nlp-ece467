from nltk.corpus import treebank

def join_punctuation(seq, characters='.,;?!%\'\"'):
    characters = set(characters)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current

'''
train_set = open("test.list", "r")
for document in train_set:
	train_document = open(str("test_set/" + document.strip()), "w")
	train_document.write(' '.join(join_punctuation(treebank.words(document.strip()))))
'''
tagset = []
train_set = open("test.list", "r")
for document in train_set:
	train_document = open(str("test_set/" + document.strip()), "w")
	tmp = treebank.tagged_words(document.strip())
	l = []
	for token in tmp:
		if token[1] != u'-NONE-':
			if token[1] not in tagset:
				tagset.append(token[1])
			l.append(token[0])
			#l.append(token[0] + "/" + token[1])
	train_document.write(' '.join(join_punctuation(l)))

print tagset
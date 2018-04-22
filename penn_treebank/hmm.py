import nltk
import math
import time
from collections import defaultdict

sos = '<s>'
eos = '</s>'
article = ['the', 'a', 'an']
preposition = ['of', 'for', 'about', 'above', 'during', 'from', 'by', 'than', 'on']
ppss = ['i', 'you']
pps = ['he', 'she']
poss = ['my', 'mine', 'your', 'yours', 'his', 'her', 'hers', 'its', 'their', 'one\'s', 'ours']

f = open("train.list", 'r')

transition = defaultdict(float)
context = defaultdict(int)
emit = defaultdict(float)

start = time.time()
for document in f:
	doc = open("train_set/" + document.strip(), 'r')
	for line in doc:
		tokens = nltk.word_tokenize(line.strip())
		previous = sos
		if sos not in context:
			context[sos] = 0
		context[sos] += 1
		for token in tokens:
			word = token.split("/")
			if len(word) == 2:
				transition_tag = previous + " " + word[1]
				emit_tag = word[1] + " " + word[0]
				emit_unk = word[1] + " <unk>"
				if transition_tag not in transition:
					transition[transition_tag] = 0
				if word[1] not in context:
					context[word[1]] = 0
				if emit_tag not in emit:
					emit[emit_tag] = 0
				#if emit_unk not in emit:
				#	emit[emit_unk] = 1

				transition[transition_tag] += 1
				context[word[1]] += 1
				emit[emit_tag] += 1
				previous = word[1]
		transition_tag = previous + " " + eos
		if transition_tag not in transition:
			transition[transition_tag] = 0
		transition[transition_tag] += 1
	doc.close()
f.close()
# end of training

for key in transition:
	token = key.split(' ')
	transition[key] /= float(context[token[0]])
	transition[key] = -math.log(transition[key])

for key in emit:
	token = key.split(' ')
	emit[key] /= float(context[token[0]])
	emit[key] = -math.log(emit[key])

end = time.time()

print "Train Time:", end - start, "(s) ellapsed."

print len(context)
print context
print sum(transition.itervalues())
print sum(emit.itervalues())


# Currently the testing of the program does not work because it might encounter words that are not in training corpus
# Smoothing techniques required to mitigate the effect of unlearned words


start = time.time()
f = open("test_set/wsj_0004.mrg", 'r')
result = open("result", 'w')

for line in f:
	words = nltk.word_tokenize(line.strip())
	if len(words) == 1:
		result.write("\n")
		continue
	l = len(words)
	print words
	# forward step
	best_score = defaultdict(float)
	best_edge = defaultdict(str)
	best_score["0 <s>"] = 0
	best_edge["0 <s>"] = None
	for i in range(0,l):
		for prev in context:
			for next in context:
				#print prev, next, words[i].lower()
				b_key = str(i) + " " + prev
				t_key = prev + " " + next
				e_key = next + " " + words[i]
				# current fix for keys not in emit. this should be modified by ngram smoothing techniques
				if e_key not in emit:
					e_key = next + " <unk>"
				if b_key in best_score and t_key in transition:
					score = best_score[b_key] + transition[t_key] + emit[e_key]
					b_key_next = str(i+1) + " " + next
					if b_key_next not in best_score:
						best_score[b_key_next] = score
						best_edge[b_key_next] = b_key
					else:
						if score > best_score[b_key_next]:
							best_score[b_key_next] = score
							best_edge[b_key_next] = b_key
	for prev in context:
		next = "</s>"
		b_key = str(l) + " " + prev
		t_key = prev + " </s>"
		e_key = "</s> " + words[i].lower()
		# current fix for keys not in emit. this should be modified by ngram smoothing techniques
		if e_key not in emit:
			e_key = "</s> <unk>"
		if b_key in best_score and t_key in transition:
			score = best_score[b_key] - math.log(transition[t_key])
			b_key_next = str(l+1) + " </s>"
			if b_key_next not in best_score:
				best_score[b_key_next] = score
				best_edge[b_key_next] = b_key
			else:
				if score > best_score[b_key_next]:
					best_score[b_key_next] = score
					best_edge[b_key_next] = b_key

	# backwards step
	tags = []
	next_edge = best_edge[str(l+1) + " </s>"]
	while next_edge != "0 <s>":
		token = next_edge.split(' ')
		position = token[0]
		tag = token[1]
		word = words[int(position) - 1]
		word_pos = word + "/" + tag
		
		if not word.isalnum() and len(word) < 3:
			word_pos = word + "/" + word
			if word == ';':
				word_pos = word + "/:"
		if word == '%':
			word_pos = word + "/NN"
		if word.isdigit():
			word_post = word + "/CD"
		if word[0] == '\'':
			word_pos = word + "/POS"
		if word.lower() in article:
			word_pos = word + "/AT"
		#if word.lower() in ppss:
			#word_pos = word + "/ppss"
		if word.lower() in pps:
			word_pos = word + "/PPS"
		if word.lower() in preposition:
			word_pos = word + "/IN"
		
		print word_pos
		tags.append(word_pos)
		next_edge = best_edge[next_edge]
	tags.reverse()
	result.write(' '.join(tags))
f.close()
result.close()

end = time.time()
print "Test Time:", end-start, "(s) ellapsed."

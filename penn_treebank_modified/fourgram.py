import nltk
import math
import time
from collections import defaultdict

f = open("train.list", 'r')

transition = defaultdict(float)
context = defaultdict(int)
emit = defaultdict(float)

start = time.time()
for document in f:
	doc = open("train_set/" + document.strip(), 'r')
	for line in doc:
		tokens = line.strip().split(" ")
		#print tokens
		prevprevprev = "<s>"
		prevprev = "<s>"
		previous = "<s>"
		if "<s>" not in context:
			context["<s>"] = 0
		context["<s>"] += 1
		for token in tokens:
			word = token.split("/")
			if len(word) == 2:
				transition_tag = prevprevprev + " " + prevprev + " " +previous + " " + word[1]
				emit_tag = word[1] + " " + word[0].lower()
				#emit_unk = word[1] + " <unk>"
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
				prevprevprev = prevprev
				prevprev = previous
				previous = word[1]

		transition_tag = prevprevprev + " " + prevprev + " " + previous + " </s>"
		if transition_tag not in transition:
			transition[transition_tag] = 0
		transition[transition_tag] += 1
	doc.close()
f.close()
# end of training
totaltrans = sum(transition.itervalues())

for key in transition:
	token = key.split(' ')
	transition[key] /= float(context[token[0]])
	transition[key] = -math.log(transition[key])
	transition[key] = round(transition[key], 3)

#for key in context:
#	context[key] += 1

for key in emit:
	token = key.split(' ')
	emit[key] /= float(context[token[0]])
	emit[key] = -math.log(emit[key])
	emit[key] = round(emit[key], 3)

end = time.time()

print transition
print "\n"
print emit
print "\n"
print context

print "Train Time:", end - start, "(s) ellapsed."

# Currently the testing of the program does not work because it might encounter words that are not in training corpus
# Smoothing techniques required to mitigate the effect of unlearned words

maxnum = max(emit.itervalues()) + 3

start = time.time()
f = open("test.list", 'r')

for testfile in f:
	test_set = open("test_set/" + testfile.strip(), 'r')
	result = open("fourgram/" + testfile.strip(), 'w')
	for line in test_set:
		words = nltk.word_tokenize(line.strip())
		#if len(words) == 1:
		#	result.write("\n")
		#	continue
		l = len(words)
		print words
		# forward step
		best_score = defaultdict(float)
		best_edge = defaultdict(str)
		best_score["0 <s>"] = 0
		best_edge["0 <s>"] = None
		for i in range(0,l):
			for prevprevprev in context:
				for prevprev in context:
					for prev in context:
						for next in context:
							#print prev, next, words[i].lower()
							b_key = str(i) + " " + prev
							prev_t = prevprevprev + " " + prevprev + " " + prev + " " + next
							e_key = next + " " + words[i].lower()
							#if e_key not in emit:
							#	e_key = next + " <unk>"
							if b_key in best_score and prev_t in transition:
								if e_key in emit:
									score = best_score[b_key] + transition[prev_t] + emit[e_key]
								else:
									score = best_score[b_key] + transition[prev_t] + maxnum
								b_key_next = str(i+1) + " " + next
								if b_key_next not in best_score:
									best_score[b_key_next] = score
									best_edge[b_key_next] = b_key
								else:
									if score < best_score[b_key_next]:
										best_score[b_key_next] = score
										best_edge[b_key_next] = b_key
		for prevprevprev in context:
			for prevrpev in context:
				for prev in context:
					next = "</s>"
					b_key = str(l) + " " + prev
					t_key = prevprevprev + " " + prevprev + " " + prev + " </s>"
					e_key = "</s> " + words[i].lower()
					# current fix for keys not in emit. this should be modified by ngram smoothing techniques
					#if e_key not in emit:
					#	e_key = "</s> <unk>"
					if b_key in best_score and t_key in transition:
						if e_key in emit:
							score = best_score[b_key] + transition[t_key] + emit[e_key]
						else:
							score = best_score[b_key] + transition[t_key] + maxnum
						b_key_next = str(l+1) + " </s>"
						if b_key_next not in best_score:
							best_score[b_key_next] = score
							best_edge[b_key_next] = b_key
						else:
							if score < best_score[b_key_next]:
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
			
			if best_edge[next_edge] != "0 <s>" and word[0].isupper():
				word_pos = word + "/NNP"
			try:
				if float(word) > float('-inf'):
					word_pos = word + "/CD"
			except:
				a = 1
			
			tags.append(word_pos)
			next_edge = best_edge[next_edge]
		tags.reverse()
		result.write(' '.join(tags) + "\n")
		print tags
	result.close()
	test_set.close()
f.close()

end = time.time()
print "Test Time:", end-start, "(s) ellapsed."

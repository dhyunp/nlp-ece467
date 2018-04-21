import nltk
from collections import defaultdict

f = open("ca09", 'r')

transition = defaultdict(float)
context = defaultdict(int)
emit = defaultdict(float)

for line in f:
	tokens = line.split(" ")
	previous = "<s>"
	for token in tokens:
		word = token.split("/")
		if len(word) == 2:
			transition_tag = previous + " " + word[1]
			emit_tag = word[1] + " " + word[0]
			if transition_tag not in transition:
				transition[transition_tag] = 0
			if word[1] not in context:
				context[word[1]] = 0
			if emit_tag not in emit:
				emit[emit_tag] = 0

			transition[transition_tag] += 1
			context[word[1]] += 1
			emit[emit_tag] += 1
			previous = word[1]
	transition_tag = previous + " </s>"
	if transition_tag not in transition:
		transition[transition_tag] = 0
	transition[transition_tag] += 1

print emit
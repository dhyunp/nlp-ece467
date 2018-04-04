corpus = "test.list"
document = open(corpus, "r")
dst = "test_set"
src = "test_label"

# still need to implement removing spaces after punctuations

for file in document:
	file = file.rstrip()
	src_file = open(src+"/"+file,"r");
	dst_file = open(dst+"/"+file,"w");
	for line in src_file:
		tokens = line.split(" ")
		write_line = ""
		for token in tokens:
			word = token.split("/")
			write_line = write_line + word[0]
			if len(word) == 2:
				if(word[1] != ".\n"):
					write_line = write_line + " "
				else:
					write_line = write_line + "\n"
		dst_file.write(write_line)
	src_file.close()
	dst_file.close()
document.close()
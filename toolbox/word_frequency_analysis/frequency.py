""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""

	#open file and read
	book = open(file_name, 'r')
	#read file line by line
	text = book.readlines()
	#isolate "START OF THIS PROJECT GUTENBERG EBOOK"
	curr_line = 0
	while text[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
	#sets text to entire document aside from isolated text
	text = text[curr_line+1:]
	#creates a string from the list (text)
	word_list = ''.join(text)
	#splits string into list of words
	word_list = word_list.split()

	#lowercase for every word
	for word in range(len(word_list)):
		word_list[word] = word_list[word].lower()

	return word_list


def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""

	#create a dictionary to count number
	word_counts = dict()

	for word in word_list:
		#adds new words into list
		if word not in word_counts:
			word_counts[word] = 1
		#word count increases if not already in
		else:
			word_counts[word] += 1

	#sorts from highest to lower count
	ordered_by_frequency = sorted(word_counts, key=word_counts.get, reverse=True)

	#returns top n words with highest frequency
	return ordered_by_frequency[:n]


x = get_word_list('napoleon.txt')
print get_top_n_words(x, 100)
"""
Downloads tweets from Twitter pertaining to a certain hashtag and recommends 
another relevant hashtag based on popularity (defined by how many times it 
appears).

Name: Cindy Sun
"""

from pattern.web import Twitter	
from collections import Counter
import re




def find(tag):
	"""
	Finds content and user ID of posts with specified hashtag and saves to
	.txt file. 
	"""
	twitter = open("twitter_data.txt", "r+")
	t = Twitter(language = 'en')

	#compiles 1000 tweets with the specified tag and saves content in file
	for tweet in t.search(tag, count = 1000):
		twitter.write(str(tweet))


def others(tweets):
	"""
	Finds other hashtags mentioned in tweets.
	"""
	#regex detects words beginning with a hashtag 
	return re.findall(r"#(\w+)", tweets)

def relevant(hashtags_list):
	"""
	Finds most relevant hashtags by amount mentioned.
	>>> relevant(['a', 'b', 'c', 'd', 'c', 'd', 'd', 'd'])
	'd'
	>>> relevant(['A', 'a', 'b', 'B', 'b'])
	'b'
	""" 
	x = 0
	relevant = ''
	for i in range(len(hashtags_list)):
		if hashtags_list.count(hashtags_list[i].lower()) > x:
			x = hashtags_list.count(hashtags_list[i].lower())
			relevant = hashtags_list[i].lower()
		elif hashtags_list.count(hashtags_list[i].lower()) == 0:
			relevant = hashtags_list
	return relevant

def recommend(key):
	"""
	Implements all functions and returns the user ID and hashtags that
	include the relevant hashtag.
	"""
	hashtags_list = []
	simple_list = []
	#opens txt file and separates tweets into lines
	twitter = open("twitter_data.txt", "r")
	tweets = twitter.readlines()
 
	for tweet in tweets:
		hashtags_list.extend(others(tweet))

	simple_list = [hashtags.lower() for hashtags in hashtags_list if not (hashtags.lower() == key)]
	print relevant(simple_list)


	


#f.write(find("#nimoy")) 
#print f.read()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

find("#nemtsov")

recommend("nemtsov")
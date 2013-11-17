import math
import csv

threshold = 2

def get_feature_dict_from_corpus(file):
    #Uses tf-idf to determine what words to use as features.
    fp = open( file, 'rb' )
    reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
    tweets = []
    for row in reader:
        tweets.append(row[3])
    
    numberOfTweets = len(tweets)
    wordCount = {}
    wordIndex = {}
    index = 0
    
    allTheWords = set()
    for tweet in tweets:
	for word in set(tweet.split()):
            if word not in wordCount:
                wordCount[word] = 1
            else:
                wordCount[word] += 1
            allTheWords.add(word)
		
    for word in (allTheWords.copy()):
	tf = 1
	idf = math.log(numberOfTweets/wordCount[word], 2)
	if (tf * idf) < threshold:
            allTheWords.remove(word)
		
    for word in allTheWords:
	wordIndex[word] = index
        index += 1
	
    return wordIndex


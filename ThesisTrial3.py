import tweepy
import sys
from tweepy import Stream
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk import bigrams

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)

###Reading your own timeline
##for status in tweepy.Cursor(api.home_timeline).items(10):
##    #process a single status
##    print(status.text)
##
###same as above but witten differently
##
##for status in tweepy.Cursor(api.home_timeline).items(10):
##    try:
##        print(status._json)
##    except Exception as ex:
##        print(ex)
##
###print friends
##
##for friend in tweepy.Cursor(api.friends).items():
##    try:
##        print(friend._json)
##    except Exception as ex:
##        print(ex)
##
##
##for tweet in tweepy.Cursor(api.user_timeline).items():
##    try:
##        print(tweet._json)
##    except Exception as ex:
##        print(ex)

#Streaming

##class MyListener(StreamListener):
##
##    def on_data(self,data):
##        try:
##            with open('mytweets.json','a') as f:
##                f.write(data)
##                return True
##        except BaseException as e:
##                print("Error on_data: %s" % str(e))
##                return True
##twitter_stream=Stream(auth,MyListener())
##twitter_stream.filter(track=['Selena Gomez'], languages=["en"])

##with open('mytweets.json','r') as f:
##    line=f.readline()
##    tweet=json.loads(line)
##    print(json.dumps(tweet, indent=4))
##
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
punctuation=list(string.punctuation)
stop=stopwords.words('english')+punctuation+['rt','RT']
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

##with open('mytweets.json', 'r') as f:
##    for line in f:
##        try:
##            tweet = json.loads(line, strict=False) ##This line is creating problems
##            try:
##                tokens = preprocess(tweet['text'])
##                print(tokens)
##                print('\n')
##            except Exception as ex:
##                print(ex)
##        except Exception as e:
##            print(e)

fname='mytweets.json'
with open(fname,'r') as f:
    count_all=Counter()
    count_hash=Counter()
    count_bigrams=Counter()
    for line in f:
        try:
            tweet=json.loads(line)
            #Create a list with all the terms
            terms_all = [term for term in preprocess(tweet['text'])]
            #Create list of all terms except stop-words and mentions
            terms_except_stop = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('@'))]
            count_all.update(terms_except_stop)
            #Creating list of bigrams
            terms_bigram= bigrams(terms_all)
            count_bigrams.update(terms_bigram)
            #Create a list of hashtags
            terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
            count_hash.update(terms_hash)
        except Exception as e:
            print(e)
    print(count_all.most_common(5))
    print(count_hash.most_common(5))
    print(count_bigrams.most_common(5))

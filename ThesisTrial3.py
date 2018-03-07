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
from collections import defaultdict

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

com=defaultdict(lambda:defaultdict(int))
fname='mytweets.json'
with open(fname,'r') as f:
    count_all=Counter()
    count_hash=Counter()
    count_bigrams=Counter()
    for line in f:
        try:
            tweet=json.loads(line)
            terms_only=[term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#','@'))]
            for i in range(len(terms_only)-1):
                for j in range(i+1, len(terms_only)):
                    w1,w2=sorted([terms_only[i],terms_only[j]])
                    if w1!= w2:
                        com[w1][w2]+=1
        except Exception as e:
            print(e)

com_max=[]
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms=sorted(com[t1].items(),key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1,t2),t2_count))
# Get the most frequent co-occurrences
terms_max=sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])

##search_word=sys.argv[1]
##count_search=Counter()
##fname='mytweets.json'
##with open(fname,'r') as f:
##    try:
##        for line in f:
##            tweet= json.loads(line)
##            terms_only=[term for term in preprocess (tweet['text']) if term not in stop and not term.startswith(('#','@'))]
##            if search_word in terms_only:
##                count_search.update(terms_only)
##    except Exception as e:
##        print(e)
##print("Co-occurance for %s:" % search_word)
##print(count_search.most_common(20))

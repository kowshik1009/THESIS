#Next step is finding out how to get the retweeters.
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
import vincent
import pandas
import math
import twitter
from twitter import *

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)

statuses=api.user_timeline('ReallySwara', include_rts=True)
for tweet in statuses:
    print(tweet.text)
    print("reweeted by:")
    who_all_retweeted=api.retweeters(tweet.id)
    for single_retweeter in who_all_retweeted:
        print(api.get_user(single_retweeter).screen_name)
    print("\n")
    

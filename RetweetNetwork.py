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
import networkx as nx
from matplotlib import pyplot

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)

graph=nx.DiGraph()
username='ReallySwara'
central_node=graph.add_node(username)
who_all_retweeted=[]
whom_the_user_retweeted=[]

statuses=api.user_timeline(username, include_rts=True)
for tweet in statuses:
    if hasattr(tweet, 'retweeted_status'):
        whom_the_user_retweeted.append(tweet.retweeted_status.author.screen_name)
    else:
        who_all_retweeted.extend(api.retweeters(tweet.id))
for single_retweeter in set(who_all_retweeted):
##        print(api.get_user(single_retweeter).screen_name)
    graph.add_edge(api.get_user(single_retweeter).screen_name,central_node)

for user in set(whom_the_user_retweeted):
    graph.add_edge(central_node,user)

pos = nx.spring_layout(graph,k=5.0,iterations=20)
nx.draw(graph,pos, with_labels=True, font_size=5, node_size=50)
pyplot.show()
    

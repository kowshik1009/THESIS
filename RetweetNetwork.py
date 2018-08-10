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
#import vincent
#import pandas
import math
import twitter
from twitter import *
import networkx as nx
import os
from matplotlib import pyplot

#Authentication

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)
api.wait_on_rate_limit=True

#Code for writing edges in file

##nx.write_edgelist(graph,'salman.txt')
###Code for reading graph from file
##g=nx.read_edgelist('JustinTrudeauRTNetwork.txt', create_using=nx.DiGraph())
##print(nx.info(g))
##pos = nx.spring_layout(g,k=5.0,iterations=20)
##nx.draw(g,pos, with_labels=True, font_size=5, node_size=50)
##pyplot.show()

#Initializing DiGraph 
graph=nx.DiGraph()
pos = nx.spring_layout(graph,k=5.0,iterations=20) #visualization parameter

#Initializing Graph variables
username='nkjemisin'
user_id=api.get_user(username).id
who_all_retweeted=[]
whom_the_user_retweeted=[]
author_retweeters=[]

#Capturing the Timelines of the central node in the graph & storing them in a File
##statuses=api.user_timeline(username, include_rts=True)
##with open(username+".txt","w+") as file:
##    for tweet in statuses:
##        file.write(str(tweet.id)+'\n')
##
##if not os.path.exists("C:\Python34\\"+username):
##    os.makedirs("C:\Python34\\"+username)

#Going through the saved tweet ids, storing the rwtweetwr ids in a tile named after the tweet id
##with open(username+".txt","r") as file:
##    for id in file.read().splitlines():
##        retweeters=api.retweeters(int(id))
##        if len(retweeters)!=0:
##            author_retweeters=retweeters
##            author_retweeters.append(user_id)
##            with open("C:\Python34\\"+username+"\\"+id+".txt","w+") as file2:
##                for a_r in author_retweeters:
##                    file2.writelines(str(a_r)+'\n')

#Creating the retweet network
author_retweeters2=[]
for filename in os.listdir("C:\Python34\\"+username):
    tweet_id=filename.partition(".")[0]
    with open("C:\Python34\\"+username+"\\"+filename,"r") as file:
        for a_r in file.read().splitlines():
            author_retweeters2.append(a_r)
    for i in range (0,len(author_retweeters2)-1):
        for j in range (i+1,len(author_retweeters2)):
            try:
                friendship=api.show_friendship(source_id=author_retweeters2[i], target_id=author_retweeters2[j])
                if friendship[0].following==True:
                    graph.add_edge(author_retweeters2[i], author_retweeters2[j], tid=tweet_id)
                elif friendship[1].following==True:
                    graph.add_edge(author_retweeters2[j], author_retweeters2[i], tid=tweet_id)
                nx.write_edgelist(graph,username+'RTNetwork2.txt')                    
            except Exception as e:
                print(e)
                continue


##pos = nx.spring_layout(graph,k=5.0,iterations=20)
##nx.draw(graph,pos, with_labels=True, font_size=5, node_size=50)
##pyplot.show()

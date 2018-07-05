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

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)
api.wait_on_rate_limit=True

###Code for writing edges in file
##nx.write_edgelist(graph,'salman.txt')
###Code for reading graph from file
##g=nx.read_edgelist('JustinTrudeauRTNetwork.txt', create_using=nx.DiGraph())
##print(nx.info(g))
##pos = nx.spring_layout(g,k=5.0,iterations=20)
##nx.draw(g,pos, with_labels=True, font_size=5, node_size=50)
##pyplot.show()

graph=nx.DiGraph()
pos = nx.spring_layout(graph,k=5.0,iterations=20)
username='nkjemisin'
user_id=api.get_user(username).id
who_all_retweeted=[]
whom_the_user_retweeted=[]
author_retweeters=[]

##statuses=api.user_timeline(username, include_rts=True)
##with open(username+".txt","w+") as file:
##    for tweet in statuses:
##        file.write(str(tweet.id)+'\n')
##
##if not os.path.exists("C:\Python34\\"+username):
##    os.makedirs("C:\Python34\\"+username)

##with open(username+".txt","r") as file:
##    for id in file.read().splitlines():
##        retweeters=api.retweeters(int(id))
##        if len(retweeters)!=0:
##            author_retweeters=retweeters
##            author_retweeters.append(user_id)
##            with open("C:\Python34\\"+username+"\\"+id+".txt","w+") as file2:
##                for a_r in author_retweeters:
##                    file2.writelines(str(a_r)+'\n')

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
#Printing out the user id of the retweeters of a certain tweet. Tomorrow I'll need to go through each one of them to build a network file.

##for tweet in statuses:
####    who_all_retweeted.extend(api.retweeters(tweet.id))
##    who_all_retweeted=api.retweeters(tweet.id)
##    author=tweet.user.id
##    author_retweeters.extend(who_all_retweeted)
##    author_retweeters.append(author)
##    for ar in author_retweeters:
##        for i in range (0,len(author_retweeters)):
##            for j in range (1,len(author_retweeters)):
##                try:
##                    if api.show_friendship(source_id=author_retweeters[i], target_id=author_retweeters[j])[0].following==True:
##                        graph.add_edge(api.get_user(author_retweeters[i]).screen_name, api.get_user(author_retweeters[j]).screen_name)
##                    elif api.show_friendship(source_id=author_retweeters[i], target_id=author_retweeters[j])[1].following==True:
##                        graph.add_edge(api.get_user(author_retweeters[j]).screen_name, api.get_user(author_retweeters[i]).screen_name)
##                    nx.write_edgelist(graph,'JustinTrudeauRTNetwork.txt')                    
##                except Exception as e:
##                    print(e)
##                    time.sleep(30)
##                    continue



            


##            nx.write_edgelist(graph,'trudeau2.txt')
##
##
##
##pos = nx.spring_layout(graph,k=5.0,iterations=20)
##nx.draw(graph,pos, with_labels=True, font_size=5, node_size=50)
##pyplot.show()
##
##nx.write_edgelist(graph,'trial.txt')    
##            
##for single_retweeter in set(who_all_retweeted):
####        print(api.get_user(single_retweeter).screen_name)
##    graph.add_edge(api.get_user(single_retweeter).screen_name,central_node)
##
##for user in set(whom_the_user_retweeted):
##    graph.add_edge(central_node,user)
##
##    

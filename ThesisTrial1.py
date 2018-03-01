import tweepy
import sys
from tweepy import Stream
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

ckey='1Ks0gAinLy8N7ive0JR4LivSm'
csecret='bm3MuSsIP2YL48VH9v6Ml4SdraFQwDpTqdRolpNLVBONvdwOjB'
atoken='965800445666054144-k0uwPi9KT8lzb0lMq298b9Az0Pl1Fpj'
asecret='9DBh4HUmLeYcBGlvXxp1Fig8mLcv9Lvr7auFcoCGhNHAb'

auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
api=tweepy.API(auth)

class listener(StreamListener):
    def on_data(self, raw_data):
        try:
            tweet_text=raw_data.lower().split('"text":"')[1].split('","source":"')[0].replace(",","")
            screen_name= raw_data.lower().split('"screen_name":"')[1].split('","location"')[0].replace("'","")
            tweet_cid=raw_data.split('"id":')[1].split('"id_str":')[0].replace(",","")

            accs=['twitter', 'twittersupport']  #banned account screen name goes in here
            words=['hate','derp'] #banned words go in here

            if not any(acc in screen_name.lower() for acc in accs):
                if not any(word in tweet_text.lower() for word in words):
                    #call what you want to do here
                    #fave(tweet_cid)
                    return True
        except Exception as e:
            print(str(e)) #prints the error message
            pass

    def on_error(self,status_code):
        try:
            print("error"+status_code)
        except Exception as e:
            print(str(e))
            pass
def retweet(tweet_cid):
    try:
        api.retweet(tweet_cid)
    except Exception as e:
        print(str(e))
        pass

def fav(tweet_cid):
    try:
        api.create_favorite(tweet_cid)
    except Exception as e:
        print(str(e))
        pass

def unfav(tweet_cid):
    try:
        api.retweet(tweet_cid)
    except Exception as e:
        print(str(e))
        pass

def tweet(myinput):
    try:
        api.update_status(myinput)
    except Exception as e:
        print(str(e))
        pass

track_words=["Red Sparrow"]
follow_acc=['2312312','1234332']

try:
    twt=Stream(auth,listener())
    twt.filter(track=track_words)
except Exception as e:
    print(str(e))
    pass
                           
                   
    

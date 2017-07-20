import tweepy
import json
import time
from datetime import datetime
#import logging
from pymongo import MongoClient
from credentials_twitter import *
from liveTweetConfig import *

#this is for live tweets and does not take past tweets
#extending tweepy's StreamListener
class MyListener(tweepy.StreamListener):
    
    def __init__(self, time_limit):
        self.start_time = time.time()
        #set time limit in terms of seconds
        self.limit = time_limit
        super(MyListener, self).__init__()
    
    #not a compulsory component
    def on_connect(self):
        """Called when the connection is made"""
        print "You're connected to the streaming server."
        print "Time now is: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
    def on_error(self, status_code):
        """This is called when an error occurs"""
        print "Error: " + status_code
        #to stop the stream
        return False
 
    def on_data(self, data):
        """This will be called each time we receive stream data"""
        connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
        db = connection[MONGODB_DB]
        collection= db[MONGODB_COLLECTION]
        #logger = logging.getLogger('customLog')
        # Decode JSON
        datajson = json.loads(data)
 
        # We only want to store tweets in Spanish
        #if "lang" in datajson and datajson["lang"] == "es":
        # Store tweet info into the fashion collection
        if (time.time() - self.start_time) < self.limit:
            #collection.insert(datajson)
            collection.update({'id':datajson['id']},datajson,upsert=True)
            #logger.info("Tweet added to MongoDB!")
            print "Tweet with id " + str(datajson['id']) + " updated in MongoDB!"
            return True
        else:
            #logger.info("TIME LIMIT REACHED, THANK YOU!")
            print "TIME LIMIT REACHED, THANK YOU!"
            print "Time now is: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return False
 
#Authenticating
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#listening based on stop words in text
api = tweepy.API(wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
listener = MyListener(time_limit=timeLimit)
streamer = tweepy.Stream(auth, listener)

#extracting keywords
array=[]
with open(KEYWORDS_PATH) as file:
    for word in file:
        array.append(word.strip())

streamer.filter(track=array)
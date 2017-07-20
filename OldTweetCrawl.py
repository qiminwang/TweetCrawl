import tweepy
import json
from credentials_twitter import *
from oldTweetConfig import *
from pymongo import MongoClient

connection = MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
collection= db[MONGODB_COLLECTION]

#Authenticating
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Extracting keywords
query=""
with open(KEYWORDS_PATH) as file:
    for word in file:
        query += word.strip()+ " OR "
query = query.rstrip(" OR ")

maxPerQuery=100 #max limit is 100 per API query
count=0

while count<maxTweets:   
    try:
        
        if (maxId<0):
            if (not sinceId):
                new_tweets = api.search(q=query, count=maxPerQuery)
            else:
                new_tweets = api.search(q=query, count=maxPerQuery, since_id=sinceId)
        else:
            if (not sinceId):
                new_tweets = api.search(q=query, count=maxPerQuery, max_id=(maxId-1))
            else:
                new_tweets = api.search(q=query, count=maxPerQuery, max_id=maxId, since_id=sinceId)
        
        if (not new_tweets):
            print "No more tweets found"
            break
        
        for tweet in new_tweets:
            datajson = tweet._json
            collection.update({'id':datajson['id']},datajson,upsert=True)
            #print str(count+1) + " Tweet with id " + str(datajson['id']) + " updated in MongoDB!"
            count+=1

        print str(count+1)+"number of tweets added"
        maxId=new_tweets[-1].id
    
    except tweepy.TweepError as e:
        # Just exit if any error
        print("Error : " + str(e))
        break
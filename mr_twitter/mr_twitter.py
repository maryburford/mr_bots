import tweepy
from textwrap import TextWrapper
import json
from itertools import cycle
from collections import deque
import json
import urllib2
from pprint import pprint
import time
import csv
from pprint import pprint
from random import randint
import sys
 
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
 
def fav_a_tweet(tweet_id):
    api.create_favorite(tweet_id)
 
def follow(user_id):
    api.create_friendship(user_id, follow=True)

def getfollowers(screen_name):
    r = api.followers_ids(screen_name)
    return r


def gettweets(user_id):
    r = api.user_timeline(user_id)
    return r
 
def gettags(tag):
    tagged = []
    result_type='recent'
    geocode='40.711874,-73.964188,10000km'
    response = tweepy.Cursor(api.search, q=tag, result_type=result_type, geocode=geocode)
    for i in response.items():
        tweet_id = i.id
        user_id = i.author.id
        user_name = i.author.name
        print response.items()
        tagged.append([tweet_id, user_id, user_name])
        return tagged 

csvfile = open('log.csv', 'ab')
log_fav_fan = csv.writer(csvfile, delimiter=',')
 
readfile = open('log.csv', 'rb')
logreader = csv.reader(readfile, delimiter=',')
 
seenmedia = {}
for row in logreader:
        media_id_seen = str(row[0]).strip()
        seenmedia[media_id_seen] = True

while True:

    array = getfollowers('Horse_ebooks')
    for i in array:
        print i
        
        try:

            response = gettweets(str(i))
            media_id = response[0].id
            if str(media_id) in seenmedia.keys():
                
                print 'already favd '
                print 'sleeping for 1 seconds'
                print
                time.sleep(1)
            else:
            
                json_object = response[0]._json
                user_name = json_object['user']['screen_name']
               # name = response[0].screen_name
                print '----'
                print 'trying to fav '+user_name
                print '---'
                seenmedia[media_id] = True
                fav_a_tweet(media_id)
                log_fav_fan.writerow([media_id,user_name,i,time.strftime("%x")])
            
                time.sleep(30)
    
              #  print time.strftime("%x")
               # print 'faved '+user_name
        except Exception, e:
            print str(e)
            time.sleep(5)


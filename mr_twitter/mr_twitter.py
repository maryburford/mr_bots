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
import argparse
 

class MR_Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	self.api = tweepy.API(auth)

    def fav_a_tweet(self, tweet_id):
	self.api.create_favorite(tweet_id)
     
    def follow(self,user_id):
	self.api.create_friendship(user_id, follow=True)

    def getfollowers(self, screen_name):
	r = self.api.followers_ids(screen_name)
	return r


    def gettweets(self,user_id):
	r = self.api.user_timeline(user_id)
	return r
     
    def gettags(self,tag):
	tagged = []
	result_type='recent'
	geocode='40.711874,-73.964188,10000km'
	response = tweepy.Cursor(self.api.search, q=tag, result_type=result_type, geocode=geocode)
	for i in response.items():
	    tweet_id = i.id
	    user_id = i.author.id
	    user_name = i.author.name
	    print response.items()
	    tagged.append([tweet_id, user_id, user_name])
	    return tagged 


    def run(self, target):
	csvfile = open('log.csv', 'ab')
	log_fav_fan = csv.writer(csvfile, delimiter=',')
	 
	readfile = open('log.csv', 'rb')
	logreader = csv.reader(readfile, delimiter=',')
	 
	seenmedia = {}
	for row in logreader:
		media_id_seen = str(row[0]).strip()
		seenmedia[media_id_seen] = True

	while True:

	    array = self.getfollowers(target)
	    for i in array:
		print i
		
		try:

		    response = self.gettweets(str(i))
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
			self.fav_a_tweet(media_id)
			log_fav_fan.writerow([media_id,user_name,i,time.strftime("%x")])
		    
			time.sleep(30)
	    
		      #  print time.strftime("%x")
		       # print 'faved '+user_name
		except Exception, e:
		    print str(e)
		    time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MR_Twitter")
    parser.add_argument("--consumer_key")
    parser.add_argument("--consumer_secret")
    parser.add_argument("--access_token_key")
    parser.add_argument("--access_token_secret")
    parser.add_argument("--target")

    args = parser.parse_args()


    if args.consumer_key and args.consumer_secret and args.access_token_key and args.access_token_secret and args.target:
	mrt = MR_Twitter(args.consumer_key, args.consumer_secret, args.access_token_key, args.access_token_secret)
	mrt.run(args.target)
    else:
	print "Must supply twitter credentials and a target."


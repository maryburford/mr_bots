from itertools import cycle
from collections import deque
import json
import urllib2
from pprint import pprint
import time
import csv	
from pprint import pprint
from random import randint
from instagram.client import InstagramAPI
import sys

class TokenGenerator:
    tokens = []
    token_index = 0

    def getToken(self):
    	self.token_index = (self.token_index + 1) % len(self.tokens)
    	return self.tokens[self.token_index]
	

def fav_a_post(media_id,token):
	print token
	api = InstagramAPI(access_token=token)
	like = api.like_media(media_id)
	return like

def post_comment(media_id,text,token):
	print token
	api = InstagramAPI(access_token=token)
	comment = api.create_media_comment(media_id, text)
	return comment

def gettags(tag):
	tagged = []
	token = tokens.getToken()
	print token
	url = 'https://api.instagram.com/v1/tags/'+tag+'/media/recent?access_token='+token+'&count=500'
	response = urllib2.urlopen(url)
	data = json.loads(response.read())
	posts = data['data']
	for i in posts:
		media_id = i['id']
		user_id = i['user']['id']
		user_name = i['user']['username']
	 	tagged.append([media_id, user_id, user_name])
	return tagged




readfile = open('car_log.csv', 'rb')
logreader = csv.reader(readfile, delimiter=',')
seenusers = {}
for row in logreader:
	media_id_seen = str(row[1]).strip()
	seenusers[media_id_seen] = True


csvfile = open('car_log.csv', 'ab')
log_fav_fan = csv.writer(csvfile, delimiter=',')



readfile = open('car_log.csv', 'rb')
logreader = csv.reader(readfile, delimiter=',')

seenmedia = {}
for row in logreader:
	media_id_seen = str(row[0]).strip()
	seenmedia[media_id_seen] = True
csvfile = open('car_log.csv', 'ab')
log = csv.writer(csvfile, delimiter=',')
tokens = TokenGenerator()	
while True:
	
	tags = ['sxsw','brooklyn','williamsburg','wholefoods']
	#tags = ['smithcollege','basic','starbucks','AlphaChiOmega','AlphaDeltaPi','AlphaPhi','ChiOmega','DeltaDeltaDelta','DeltaGamma','GammaPhiBeta','KappaAlphaTheta','KappaDelta','KappaKappaGamma','PiBetaPhi','AlphaGammaDelta','DeltaZeta','KappaKappaGamma','PhiMu','SigmaKappa']
	for i in tags:
		medias = gettags(i)
		print 'getting new media to robo-fav'

		time.sleep(10)
		print
		for media in medias:
			media_id = media[0]
			user_id = media[1]
			user_name = media[2]
			if media_id in seenmedia.keys():
				
				print 'already favd '+user_id+' '+user_name+' '+i
				print 'sleeping for 1 seconds'
				print
				time.sleep(1)
				
			else:
				try:	

			
					token = tokens.getToken()
					print token
					print fav_a_post(media_id,token)
					print time.strftime("%x")
					print 'faved '+user_name+' '+media_id+' '+i
					seenmedia[media_id] = True
					log.writerow([media_id,user_id,user_name,i,time.strftime("%x")])
			
					print 'sleeping for 60 seconds'
					print
			
					time.sleep(95)
				except KeyboardInterrupt:
					sys.exit()
				except Exception, e:
					print str(e)
					if 'Rate limited-Your' in str(e):
						print 'rate limited..sleeping.. '+user_name+' '+i
						time.sleep(900)
					else:
						print 'error'
						
						time.sleep(3600)
						print
						pass
							
					


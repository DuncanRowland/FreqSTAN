#!/usr/bin/env python

from secrets import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

from twython import Twython
from time import strftime
from subprocess import call
from sys import argv
from os import remove

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweet_id = argv[1]
tweet_screen_name = argv[2]

filename = tweet_id+'.jpg'
cmd=['./fswebcam.sh','-r','640x480','-d','/dev/video0','-i','0','--no-banner','-q',filename]
call(cmd)
photo = open(filename, 'rb')
image_ids = twitter.upload_media(media=photo)
status = "@"+tweet_screen_name+" Welcome "+strftime("%Y-%m-%d %H:%M:%S")
twitter.update_status(status=status, media_ids=image_ids['media_id'], in_reply_to_status_id=tweet_id)
remove(filename)


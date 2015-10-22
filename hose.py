#!/usr/bin/env python

from secrets import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from entropy import InfoSize, numberToBase

from twython import TwythonStreamer
from time import sleep
import requests
import json

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            text = data['text'].encode('utf-8')
            print(text)
            s=InfoSize(text)

            url="http://localhost:8080"
            id=0
            bits = numberToBase(s,2)
            bits.reverse()
            for bit in bits:
               if bit==0:
                  cmd = [{'id':str(id),'target':0}]
               else:
                  cmd = [{'id':str(id),'target':100}]
               payload = {'data':json.dumps(cmd)}
               requests.post(url, data=payload)
               id+=1
               if(id>1):
                  break

    def on_error(self, status_code, data):
        print(status_code)
        print("Rate limited, sleeping for 600")
        sleep(600)

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='#freq')
#stream.user()


#!/usr/bin/env python

from secrets import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

from twython import TwythonStreamer
from time import sleep
import math
import requests
import json

#Shannon Entropy -> minimum bits per symbol -> * message length = minimum bits needed to encode message
def InfoSize(st):
   stList = list(st)
   alphabet = list(set(stList))
   freqList = []
   for symbol in alphabet:
       ctr = 0
       for sym in stList:
           if sym == symbol:
               ctr += 1
       freqList.append(float(ctr) / len(stList))
   ent = 0.0
   for freq in freqList:
       ent = ent + freq * math.log(freq, 2)
   ent = -ent
   mbps = int(math.ceil(ent))
   return mbps*len(stList)

#Convert to base in list form
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n /= b
    return digits[::-1]

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            text = data['text'].encode('utf-8')
            print(text)
            s=InfoSize(text)

            url="http://localhost:43210"
            id=0
            bits = numberToBase(s,2)
            bits.reverse()
            for bit in bits:
               if bit==0:
                  cmd = [{'id':str(id),'target':2500}]
               else:
                  cmd = [{'id':str(id),'target':3500}]
               payload = {'data':json.dumps(cmd)}
               requests.post(url, data=payload)
               id+=1
               if(id>1):
                  break

    def on_error(self, status_code, data):
        print(status_code)
        print("Rate limited, sleeping for 3000")
        sleep(3000)

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='#love')
#stream.user()


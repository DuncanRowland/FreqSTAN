#!/usr/bin/env python

from scripts import scripts
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
      if ('id' in data) and \
         ('in_reply_to_screen_name' in data) and \
         (str(data['in_reply_to_screen_name']).upper() == 'PILAMP') and \
         ('user' in data) and \
         ('screen_name' in data['user']) and \
         ('text' in data):
         
         text_upper = data['text'].encode('utf-8').upper()
         tweet_id = str(data['id'])
         tweet_screen_name = data['user']['screen_name']
        
         if 'SNAP' in text_upper:
           print("take photo")
           return 
            #Take photo
         
         cmds=list()
         for script_name in scripts:
            if script_name in text_upper:
               print("do script: "+script_name)
               cmds = scripts[script_name]
               break
        
         if cmds==list():
            print("do entropy (parallel)") 
            s=InfoSize(data['text'].encode('utf-8'))
            id=0
            bits = numberToBase(s,2)
            bits.reverse()
            cmds = list()
            for bit in bits:
               if bit==0:
                  cmds.append({'id':str(id),'target':2500})
               else:
                  cmds.append({'id':str(id),'target':3500})
               id+=1
               if(id>1):
                  break

         url="http://localhost:43210"
         payload = {'data':json.dumps(cmds)}
         print(payload)
         requests.post(url, data=payload)

    def on_error(self, status_code, data):
        print(status_code)
        print("Rate limited, sleeping for 3000")
        sleep(3000)

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.user()


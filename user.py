#!/usr/bin/env python

from scripts import scripts
from secrets import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from entropy import InfoSize, numberToBase

from twython import TwythonStreamer
from time import sleep
from subprocess import Popen
import requests
import json

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
            cmd=['./snap.py', tweet_id, tweet_screen_name]
 	    Popen(cmd)
            return
 
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
                  cmds.append({'id':str(id),'target':0})
               else:
                  cmds.append({'id':str(id),'target':100})
               id+=1
               if(id>1):
                  break

         url="http://localhost:8080"
         payload = {'data':json.dumps(cmds)}
         print(payload)
         requests.post(url, data=payload)

    def on_error(self, status_code, data):
        print(status_code)
        print("Rate limited, sleeping for 600")
        sleep(600)

stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.user()


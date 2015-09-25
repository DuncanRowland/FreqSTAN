#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
from time import time
import json

jrk = Popen(['sudo', '/home/pi/pololu-usb-sdk/Jrk/JrkCmd/JrkCmd'], stdin=PIPE, stdout=PIPE)

cmds = list()

Ids = {'0','1','2','3','4','5','6','7','8','9'}
Stopped = set()
StoppedAt = dict()
Pending = list()

def isStopped(id):
   if id in Pending:
      return False;
   jrk.stdin.write(id+'\n')
   c = jrk.stdout.readline()
   return c == '0\n' or c == '-1\n'

def delaysExpired(cmd):
   now = time()
   for c in cmd:
      if now < StoppedAt[c['id']] + c.get('delay',5):
         return False
   return True

def setTargetCallback(id, target):
   jrk.stdin.write(id+" "+target+"\n")
   if id in Stopped:
      Stopped.remove(id)
   Pending.remove(id)
 
def setTargets(cmd):
   for c in cmd:
      loop.call_later( \
         c.get('pause',0), \
         setTargetCallback, \
         c['id'], \
         str(c['target']) \
      )
      Pending.append(c['id'])

def getIds(cmd):
   idAcc = set()
   for c in cmd:
      idAcc.add(c['id'])
   return idAcc

def processMotors():
   global jrk

   if not jrk:
      print("Err: jrk closed")

   for id in Ids-Stopped:
      if isStopped(id):
         Stopped.add(id)
         StoppedAt[id]=time()

   idAcc = set()
   for cmd in cmds[:]:
      ids = getIds(cmd)

      #Make sure all motors have stopped
      if not ids <= Stopped:
         continue

      #Make sure no ids have already appeared in earlier cmds
      idCmp = idAcc.copy()
      idAcc |= ids
      if ids & idCmp:
         continue 

      #Make sure all delays have expired
      if not delaysExpired(cmd):
         continue

      #Set targets 
      setTargets(cmd)

      #Remove executed command
      cmds.remove(cmd)

import tornado.httpserver
import tornado.ioloop
import tornado.web

class requestHandler(tornado.web.RequestHandler):
   def get(self):
      self.write(open('./index.html',"r").read())
   def post(self):
      self.write(open('./index.html',"r").read())
      data = self.get_argument('data')
      obj = json.loads(data)
      if len(obj)==1:
         if len(cmds)<10:
            cmds.append(obj)
         #Otherwise lose all single commands (but keep command groups)
      else:
         i=0
         for c in cmds:
            if len(c)==1:
               break
            i+=1
         cmds.insert(i,obj)

application = tornado.web.Application([
   (r'/', requestHandler),
])

if __name__ == "__main__":
   http_server = tornado.httpserver.HTTPServer(application)
   http_server.listen(43210) #Use a sensible port number here*
   tornado.ioloop.PeriodicCallback(processMotors, 1000).start()
   loop=tornado.ioloop.IOLoop.instance()
   loop.start()

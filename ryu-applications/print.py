import ast
import sys
import json
import requests
import time
import os.path

def send_intent(form):
    body = json.dumps(form)
    r = requests.post("http://localhost:8080/intent/add", data=body)
    print(r.status_code, r.reason)


add_flow=False
file_exists = os.path.isfile("./arc.txt")
#print file_exists

ant_dpid = 0

while True:
 print ant_dpid
 if file_exists == True:
  x = open('arc.txt','r')
  x = x.read()
  x = ast.literal_eval(x)
  if ant_dpid != x:
   print '-------'
   print ant_dpid
   print x
   ant_dpid = x
   time.sleep(1)
  else:
   time.sleep(1) 
 else:
  time.sleep(1)
'''
'''

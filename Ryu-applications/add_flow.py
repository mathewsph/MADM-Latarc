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
# print ant_dpid
 if file_exists == True:
  x = open('arc.txt','r')
  x = x.read()
  x = ast.literal_eval(x)
  if ant_dpid != x:
   form = {'source': {'sw_src': '100', 'in_port_src': '3', 'host_src': '10.0.0.2'}, 'dest': {'sw_dst': str(x), 'in_port_dst': '1', 'host_dst': '10.0.0.10'}}
   send_intent(form)
   time.sleep(1)
   ant_dpid = x
  else:
   time.sleep(1) 
 else:
  time.sleep(1)
'''
'''
#form = {'source': {'sw_src': '1', 'in_port_src': '1', 'host_src': '10.0.0.10'}, 'dest': {'sw_dst': '3', 'in_port_dst': '3', 'host_dst': '10.0.0.101'}}
#send_intent(form)

'''list = []
for i in range( 1, 18 ):
    in_port_dst = i + 2
    temp = {}
    temp = {'source': {'sw_src': '1', 'in_port_src': '1', 'host_src': '10.0.0.10'}, 'dest': {'sw_dst': '3', 'in_port_dst': '%i' % in_port_dst, 'host_dst': '10.0.0.1%02i' % i}}
    list.append(temp)

for i in list:
    send_intent(i)


list = []
for i in range( 18, 36 ):
    in_port_dst = i - 15
    temp = {}
    temp = {'source': {'sw_src': '1', 'in_port_src': '1', 'host_src': '10.0.0.10'}, 'dest': {'sw_dst': '4', 'in_port_dst': '%i' % in_port_dst, 'host_dst': '10.0.0.1%02i' % i}}
    list.append(temp)

for i in list:
    send_intent(i)'''

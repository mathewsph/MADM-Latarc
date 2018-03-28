import json
import requests

def send_intent(form):
    body = json.dumps(form)
    r = requests.post("http://localhost:8080/intent/add", data=body)
    print(r.status_code, r.reason)

form = {'source': {'sw_src': '14', 'in_port_src': '3', 'host_src': '10.0.0.2'}, 'dest': {'sw_dst': '1', 'in_port_dst': '1', 'host_dst': '10.0.0.10'}}
send_intent(form)

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

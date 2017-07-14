# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller import ofp_handler
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import ast
from pprint import pprint
from ryu.topology.api import get_link, get_switch, get_host, get_all_host
from ryu.topology import event, switches
import struct
import threading
import socket
import os
import time
#from ryu.app import simple_switch_13
from ryu.lib import hub

class SimpleTopologyMonitor13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleTopologyMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
#        self.monitor_thread = hub.spawn(self._monitor)
        self.monitor2_thread = hub.spawn(self._monitor2)
        self.mac_to_port = {}


    @set_ev_cls(event.EventHostAdd, MAIN_DISPATCHER)
 #   def _monitor(self):
 #       while True:
 #          self.get_topology_data(self)
 #          hub.sleep(2)
    def _monitor2(self):
        while True:
           self.get_socket(self)
           hub.sleep(2)
    
    def del_flow(self, datapath, dst):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(dl_dst=addrconv.mac.text_to_bin(dst))
        mod = parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_DELETE)
        datapath.send_msg(mod)


    def get_topology_data(self, ev):
#       print self.mac_to_port
       switch_list = get_switch(self, None) #.topology_api_app
       switches=[switch.dp.id for switch in switch_list]
#       print "switches: ", switches
#       for switch in switch_list:
#          for port in switch.ports:
#              print port.name
#              print port.hw_addr
       hosts = get_host(self, None)       
#       for host in hosts:
#        if host.port.name[0] != 's' and 'eth' not in host.port.name:
##         self.logger.info('host-mac         '
#                         ' access-point  rssi           '
#                         'out-port packets  bytes')
#         self.logger.info('----------------- '
#                         '------------ ----'
#                         '--------------------------')
#         print host.mac
#         print host.port.dpid
#         print host.port.name
#         print dir(host.mac)
#       self.logger.info('----------------- '
#                         '------------ ----'
#                         '--------------------------')
    def get_socket(self, ev):
      HOST = ''              # Endereco IP do Servidor
      PORT = 15000            # Porta que o Servidor esta
      tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
      orig = (HOST, PORT)
      tcp.bind(orig)
      tcp.listen(1)
      while True:
          con, cliente = tcp.accept()
#          print 'Conectado por', cliente
          while True:
              msg = con.recv(1024)
#              rssi = msg_splitted[0]
#              rssi = rssi.replace("dBm","")
#              rssi = int(rssi)
              if not msg: break
              print msg
              switch_list = get_switch(self, None) #.topology_api_app
              switches=[switch.dp.id for switch in switch_list]
              print "switches: ", switches
              links_list = get_link(self, None)
              links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]   
              print "links", links
#                  print link
              rssi = msg.split()[0]
              rssi = int(rssi.replace("dBm",""))
              current_AP = (msg.split()[4]).split("-")[0]
              candidate_APs = ast.literal_eval(msg.split('\n')[1])
              print current_AP
              current_AP_number = int(current_AP.replace("ap",""))
              print current_AP_number
              if current_AP in candidate_APs:
                index_currentAP = candidate_APs.index(current_AP)
                del candidate_APs[index_currentAP]
              for ap in candidate_APs:
                k = candidate_APs.index(ap)
                candidate_APs[k] = int(ap.replace("ap",""))
              print candidate_APs
#              print candidate_APs[-1]
              if rssi <= -50:
                for link in links:
                 if link[1] == current_AP_number:
                  sw = link[0]
                  port_in_switch = link[2]['port']
                print sw
                str_candidate_APs = str(candidate_APs).replace(" ","")
                os.system('ovs-ofctl del-flows s' + str(sw) + ' ' + '"in_port=' + str(port_in_switch)+'"')
                os.system('ovs-ofctl del-flows s' + str(sw) + ' ' + '"dl_dst=' +  msg.split()[2]+'"')
                print "weak signal, executing handover:"
                x = "python saw_v4.py " + str(max(candidate_APs)) + " " + str_candidate_APs
#                print x
#                del_flow(self,datapath,dst)
                decision = os.popen(x)
                decision = decision.read()
                m = decision.split()[0][2]
                print m
                for link in links:
                 if link[1] == int(m):
                   decision_sw = link[0]
                   decision_port_in_switch = link[2]['port']
#                 elif link[0] == 18:
                 if rssi == -50:
                    z=open('arc.txt','w')
                    z.write(m)
                    z.close()
                print decision
                data = con.send(decision)
              else:
                data = con.send(" ") 
#          print 'Finalizando conexao do cliente', cliente
          con.close()







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
import logging
import struct
import json
import random
import ryu.utils
from webob import Response
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import mac_to_port
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import ofctl_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.controller import dpset
from ryu.topology.api import get_switch, get_link, get_host
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.topology import event, switches
import networkx as nx
from pprint import pprint
import threading
import socket
import os
import time
import ast

#from ryu.app import simple_switch_13
from ryu.lib import hub

LOG = logging.getLogger('ryu.app.simple_switch_13')

class FlowCore(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FlowCore, self).__init__(*args, **kwargs)
        self.flows = {}
        self.mac_to_port = {}
        self.ip_to_port = {}
        self.topology_api_app = self
        self.net=nx.DiGraph()
        self.nodes_1 = {}
        self.nodes_2 = {}
        self.links = {}
        self.no_of_nodes = 0
        self.no_of_links = 0
        self.i=0
        self.k=0
        self.f=0
        self.dp = None
        self.dps = {}
        self.monitor2_thread = hub.spawn(self._monitor2)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, cookie=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst, table_id=0)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst, table_id=0, idle_timeout=300)
        datapath.send_msg(mod)

    def create_intent_internal(self, body):
        sw_src = int(body['source']['sw_src'])
        sw_dst = int(body['dest']['sw_dst'])
        print sw_dst
        #sw_dst = filter_data['switch_dst']
        src = body['source']['host_src']
        dst = body['dest']['host_dst']
        print dst
        in_port_src = int(body['source']['in_port_src'])
        in_port_dst = int(body['dest']['in_port_dst'])
        #out_port_src = filter_data['out_port_src']
        #out_port_dst = filter_data['out_port_dst']
        print self.net.edges()
        if src not in self.net:
            print "src"
            self.net.add_node(src)
            self.net.add_edge(sw_src,src,{'port':in_port_src, 'flows': {}, in_port_src: {}})
            self.net.add_edge(src,sw_src,{'port':in_port_src, 'flows': {}, in_port_src: {}})
            self.net.add_edge(src,sw_src)
        if dst not in self.net:
            print "dst"
            self.net.add_node(dst)
            self.net.add_edge(sw_dst,dst,{'port':in_port_dst, 'flows': {}, in_port_dst: {}})
            self.net.add_edge(dst,sw_dst,{'port':in_port_dst, 'flows': {}, in_port_dst: {}})
            self.net.add_edge(dst,sw_dst)
            path=nx.shortest_path(self.net,src,dst)
        else:
            print "dstf"
            try:
                self.net.remove_edge(1,dst)
                self.net.remove_edge(dst,1)
                self.net.add_edge(sw_dst,dst,{'port':in_port_dst, 'flows': {}, in_port_dst: {}})
                self.net.add_edge(dst,sw_dst,{'port':in_port_dst, 'flows': {}, in_port_dst: {}})
                self.net.add_edge(dst,sw_dst)         
	        path=nx.shortest_path(self.net,src,dst)
            except Exception:
                pass

        print self.net.edges()
	path=nx.shortest_path(self.net,src,dst)
        print path
        for i in xrange(0, len(path)-1):
            dpid = path[i]
            if isinstance(dpid, int):
                datapath = self.get_datapath(dpid)
                ofproto = datapath.ofproto
                ofproto_parser = datapath.ofproto_parser
                print path[path.index(dpid)+1]
                next = path[path.index(dpid)+1]
                print next
                print path[path.index(dpid)-1]
                previous = path[path.index(dpid)-1]
                print previous
                out_port = int(self.net[dpid][next]['port'])
                print self.net[dpid]
                in_port = int(self.net[dpid][previous]['port'])
                print in_port
                actions = [ofproto_parser.OFPActionOutput(out_port)]
                filter_fields = {'in_port': in_port,'ipv4_dst': dst, 'ipv4_src': src, 'eth_type': 0x0800}
                match = ofproto_parser.OFPMatch(in_port=in_port, ipv4_dst=dst, ipv4_src=src, eth_type=0x0800)
                match1 = ofproto_parser.OFPMatch(in_port=out_port, ipv4_dst=src, ipv4_src=dst, eth_type=0x0800)
                actions1 = [ofproto_parser.OFPActionOutput(in_port)]
                self.nodes_1[dpid]=match
                self.nodes_2[dpid]=match1
                cookie = random.randint(0, 0xfffffff)
                cookie1 = random.randint(0, 0xfffffff)
                self.add_flow(datapath, 1, match, actions, cookie)
                self.add_flow(datapath, 1, match1, actions1, cookie1)

                if dpid not in self.ip_to_port:
                    self.ip_to_port.setdefault(dpid, {})

                self.ip_to_port[dpid][self.i] = match
                self.ip_to_port[dpid][self.k] = match1
            self.i += 1
            self.k += 1
        return True
#           print self.ip_to_port
#            print
        '''
        for i in xrange(0, len(path)-1):
            dpid = path[i]
            if isinstance(dpid, int):
                datapath = self.get_datapath(dpid)
                ofproto = datapath.ofproto
                ofproto_parser = datapath.ofproto_parser
                next = path[path.index(dpid)+1]
                previous = path[path.index(dpid)-1]
                out_port = int(self.net[dpid][next]['port'])
                #print out_port
                in_port = int(self.net[dpid][previous]['port'])
                actions = [ofproto_parser.OFPActionOutput(in_port)]
                #filter_fields = {'in_port': in_port,'ipv4_dst': dst, 'ipv4_src': src, 'eth_type': 0x0800}
                match1 = ofproto_parser.OFPMatch(in_port=in_port, ipv4_dst=dst, ipv4_src=src, eth_type=0x0800)
                match = ofproto_parser.OFPMatch(in_port=out_port, ipv4_dst=src, ipv4_src=dst, eth_type=0x0800)
                self.nodes_2[dpid]=match
                cookie = random.randint(0, 0xfffffff)
                self.add_flow(datapath, 1, match, actions, cookie)
                if dpid not in self.ip_to_port:
                    self.ip_to_port.setdefault(dpid, {})

                self.ip_to_port[dpid][self.i] = match

            self.i += 1
#           print self.ip_to_port
#           print
       '''
    def get_datapath(self, dpid):
        if dpid not in self.dps:
            datapath = get_switch(self.topology_api_app, dpid)[0]
            dp = datapath.dp
            self.dps[dpid] = dp
            return dp

        return self.dps[dpid]

    def del_flow(self, datapath, match):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        mod = parser.OFPFlowMod(datapath=datapath,
                                command=ofproto.OFPFC_DELETE,
                                out_port=ofproto.OFPP_ANY,
                                out_group=ofproto.OFPG_ANY,
                                match=match)
        datapath.send_msg(mod)

    def delete_intent_internal(self):
        print self.net.edges()
        '''
        if self.net[1]['10.0.0.10']:
            self.net.remove_edge(1, u'10.0.0.10')

        if self.net['10.0.0.10'][1]:
            self.net.remove_edge(u'10.0.0.10', 1)

        if self.net[7]['10.0.0.2']:
            self.net.remove_edge(7, '10.0.0.2')

        if self.net['10.0.0.2'][7]:
            self.net.remove_edge('10.0.0.2', 7)
        '''

        for dpid in self.nodes_1:
            match = self.nodes_1[dpid]
            if isinstance(dpid, int):
                datapath = self.get_datapath(dpid)
                self.del_flow(datapath, match)

        for dpid in self.nodes_2:
            match = self.nodes_2[dpid]
            if isinstance(dpid, int):
                datapath = self.get_datapath(dpid)
                self.del_flow(datapath, match)

    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self.topology_api_app, None)
        switches=[switch.dp.id for switch in switch_list]
        self.net.add_nodes_from(switches)
        links_list = get_link(self.topology_api_app, None)
        links=[(link.src.dpid,link.dst.dpid,{'flows': {},'port':link.src.port_no}) for link in links_list]
        self.net.add_edges_from(links)
        links=[(link.dst.dpid,link.src.dpid,{'flows': {},'port':link.dst.port_no}) for link in links_list]
        self.net.add_edges_from(links)
        #self.create_intent_internal(self.filter_data)

    @set_ev_cls(ofp_event.EventOFPFlowRemoved, MAIN_DISPATCHER)
    def flow_removed_handler(self, ev):
        pass
    def verify_has_flow(self, dp):
        pass
    def remove_flow_internal(self, datapath, filter_fields):
        ofproto = datapath.ofproto
        ofproto_parser = datapath.ofproto_parser
        pass

    def find_shortpath(self, src, dst):
        path=nx.shortest_path(self.net,src,dst)
        return path

    def install_flow_after_link_is_down(self, infos, ip, srcdpid, dstdpid):
        pprint('link is down... inserting new flow...')

        src = infos['ipv4_src']
        dst = infos['ipv4_dst']
        path = self.find_shortpath(src, dst)
        for i in xrange(0, len(path)-1):
            dpid = path[i]
            if isinstance(dpid, int):
                try:
                    datapath = self.get_datapath(dpid)
                    ofproto = datapath.ofproto
                    ofproto_parser = datapath.ofproto_parser
                    next = path[path.index(dpid)+1]
                    previous = path[path.index(dpid)-1]
                    out_port = int(self.net[dpid][next]['port'])
                    in_port = int(self.net[dpid][previous]['port'])
                    actions = [ofproto_parser.OFPActionOutput(out_port)]
                    filter_fields = {'in_port': in_port,'ipv4_dst': dst, 'ipv4_src': src, 'eth_type': 0x0800}
                    match = ofproto_parser.OFPMatch(in_port=in_port, ipv4_dst=dst, ipv4_src=src, eth_type=0x0800)
                    self.add_flow(datapath, 1, match, actions)
                    if dpid not in self.ip_to_port:
                        self.ip_to_port.setdefault(dpid, {})
                    self.ip_to_port[dpid][ip] = match
                    self.i += 1
                except KeyError, e:
                    continue

    @set_ev_cls(event.EventLinkDelete)
    def link_modify_handler(self, ev):
        linkfull = ev.link.to_dict()
        #pprint(ev.link.src.port_no)
        #pprint(linkfull)
        srcdpid = int(linkfull['src']['dpid'])
        dstdpid = int(linkfull['dst']['dpid'])
        src_port = int(linkfull['src']['port_no'])
        dst_port = int(linkfull['dst']['port_no'])
        datapath = self.get_datapath(srcdpid)
        dpid = datapath.id

        print srcdpid
        print dstdpid
        if self.net[srcdpid][dstdpid]:
            self.net.remove_edge(srcdpid, dstdpid)

        if dpid in self.ip_to_port:
            for ip in self.ip_to_port[dpid]:
                if datapath is None:
                    continue
                ofproto = datapath.ofproto
                ofproto_parser = datapath.ofproto_parser
                match = self.ip_to_port[dpid][ip]
                #pprint(match)
                mod = ofproto_parser.OFPFlowMod(datapath=datapath, command=ofproto.OFPFC_DELETE, match = match,
                        out_port=ofproto.OFPP_ANY,out_group=ofproto.OFPG_ANY, table_id=0)

                datapath.send_msg(mod)
#                print match,srcdpid,dstdpid
                self.install_flow_after_link_is_down(match, ip, srcdpid, dstdpid)
        del self.ip_to_port[dpid]

    @set_ev_cls(event.EventLinkAdd)
    def link_add(self, ev):
        link = ev.link
        links=[(link.src.dpid,link.dst.dpid,{'flows': {},'port':link.src.port_no})]
        src = link.src.dpid
        dst = link.dst.dpid
        if links not in self.net:
            self.net.add_edges_from(links)

    def _monitor2(self):
        while True:
           self.get_socket(self)
           hub.sleep(2)

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
              if rssi == -48:
                for link in links:
                 if link[1] == current_AP_number:
                  sw = link[0]
                  port_in_switch = link[2]['port']
                print sw
                str_candidate_APs = str(candidate_APs).replace(" ","")
#                os.system('ovs-ofctl del-flows s' + str(sw) + ' ' + '"in_port=' + str(port_in_switch)+'"')
#                os.system('ovs-ofctl del-flows s' + str(sw) + ' ' + '"dl_dst=' +  msg.split()[2]+'"')
                print "weak signal, executing handover:"
                x = "python saw.py " + str(max(candidate_APs)) + " " + str_candidate_APs
#                print x
#                del_flow(self,datapath,dst)
                decision = os.popen(x)
                decision = decision.read()
                m = decision.split()[0][2]
                if self.f == 0:
                  self.delete_intent_internal()
                  form = {'source': {'sw_src': '7', 'in_port_src': '3', 'host_src': '10.0.0.2'}, 'dest': {'sw_dst': m, 'in_port_dst': '1', 'host_dst': '10.0.0.10'}}
                  self.create_intent_internal(form)
                self.f = 1
                print m
                for link in links:
                 if link[1] == int(m):
                   decision_sw = link[0]
                   decision_port_in_switch = link[2]['port']
#                 elif link[0] == 18:
#                 if rssi == -49:
#                    z=open('arc.txt','w')
#                    z.write(m)
#                    z.close()
                print decision
                data = con.send(decision)
              else:
                data = con.send(" ") 
#          print 'Finalizando conexao do cliente', cliente
          con.close()



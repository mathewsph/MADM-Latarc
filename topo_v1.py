#!/usr/bin/python

#-51.47
"""
Setting the position of Nodes (only for Stations and Access Points) and providing mobility.

"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSKernelSwitch
import threading
import time
import os
import threading
from threading import Timer

def topology():

#    def current_ap():
#        threading.Timer(2.0,current_ap).start()
#        a = sta1.params['associatedTo'][0]
#        x = sta1.params['rssi'][0]
#        sta1_current_ap=open("sta1_current_ap.txt","w")
#        sta1_current_rssi=open("sta1_current_rssi.txt","w")
#        sta1_current_ap.write(str(a))
#        sta1_current_rssi.write(str(x))

    "Create a network."
    net = Mininet( controller=Controller, autoStaticArp=True, link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, rec_rssi=True )
#    net = Mininet( controller=Controller, link=TCLink, accessPoint=OVSKernelAP, switch=OVSKernelSwitch, rec_rssi=True )

    print "*** Creating nodes"
    h2 = net.addHost('h2', mac='00:00:00:00:00:32', ip='10.0.0.2/8' )
    h2.setARP('10.0.0.10','00:00:00:00:00:64')
#    h2.setARP('10.0.0.10','02:00:00:00:01:00')
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:64', wlans=2 )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'ap1-ssid', mode= 'g', channel= '1', position='22,50,0', ip='10.0.0.8/8' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'ap2-ssid', mode= 'g', channel= '1', position='45,50,0' )
    ap3 = net.addAccessPoint( 'ap3', ssid= 'ap3-ssid', mode= 'g', channel= '1', position='60,35,0' )
    ap4 = net.addAccessPoint( 'ap4', ssid= 'ap4-ssid', mode= 'g', channel= '1', position='75,50,0' )
    ap5 = net.addAccessPoint( 'ap5', ssid= 'ap5-ssid', mode= 'g', channel= '1', position='60,25,0' )
    ap6 = net.addAccessPoint( 'ap6', ssid= 'ap6-ssid', mode= 'g', channel= '1', position='60,45,0' )
    A = net.addSwitch('A', dpid='00007')
    B = net.addSwitch('B', dpid='00008')
    '''
    C = net.addSwitch('C', dpid='00009')
    D = net.addSwitch('D', dpid='00010')
    E = net.addSwitch('E', dpid='00011')
    F = net.addSwitch('F', dpid='00012')
    G = net.addSwitch('G', dpid='00013')
    '''
    c5 = net.addController( 'c5', controller=RemoteController, ip='127.0.0.1')
#    net.plotNode(c5, position='120,120,0')
    net.runAlternativeModule('./mac80211_hwsim.ko')

    all_aps_positions = open("aps_positions.txt","w")
    aps_pos = {}

#    apn = len(net.accessPoints)

#    for i in range(1,apn+1):
#      aps_pos['ap'+str(i)] = eval('ap'+str(i)+'.params["position"]')
#    p = str(aps_pos)
#    all_aps_positions.write(p)
#    all_aps_positions.close()
#    def getStationRange():
#       threading.Timer(1,getStationRange).start()
#       if sta1.params['rssi'][0] < -48:
#        print aps_pos
#        s=open("positions.txt","w")
#       time.sleep(2)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(A, h2, port1 = 3)
    net.addLink(A, ap1, bw=8, delay='15ms')
    net.addLink(A, ap2, bw=42, loss=1.2, jitter='10ms', delay='16ms')
    net.addLink(A, ap3, bw=27, loss=2.8, jitter='6ms', delay='11ms')
    net.addLink(A, ap4, bw=31, loss=4.6, jitter='7.0ms', delay='12ms')
    net.addLink(A, ap5, bw=21.0, loss=1.6, jitter='5.0ms', delay='13ms')
    net.addLink(A, ap6, bw=39, loss=3.0, jitter='11ms', delay='14ms')
    net.addLink(ap1, sta1)
    '''
    net.addLink(G, ap6)
    net.addLink(A, D)
    net.addLink(A, C)
    net.addLink(B, C)
    net.addLink(B, E)
    net.addLink(C, D)
    net.addLink(C, E)
    net.addLink(D, F)
    net.addLink(D, G)
    net.addLink(E, G)    

    net.addLink(A, h2, port1 = 3)
    net.addLink(A, ap1, bw=8, loss=2.0, jitter='5ms', delay='15ms')
    net.addLink(A, ap2)
    net.addLink(A, ap3)
    net.addLink(A, ap4)
    net.addLink(A, ap5)
    net.addLink(A, ap6)
    '''

#    sta1.setIP('10.0.0.10/8', intf="sta1-wlan0")
#    sta1.cmd('ip addr add 10.0.0.3/8 dev sta1-wlan0')

    sta1.setIP('10.0.0.10/8', intf="sta1-wlan0")
    sta1.setIP('10.0.0.10/8', intf="sta1-wlan1")
# ifconfig eth0 down
# ifconfig eth0 hw ether 00:80:48:BA:d1:30
# ifconfig eth0 up
    sta1.cmd("ifconfig sta1-wlan1 down")
    sta1.cmd("ifconfig sta1-wlan1 hw ether 00:00:00:00:00:64")
    sta1.cmd("ifconfig sta1-wlan1 up")

    print "*** Starting network"
    net.build()
    ap1.start( [c5] )
    ap2.start( [c5] )
    ap3.start( [c5] )
    ap4.start( [c5] )
    ap5.start( [c5] )
    ap6.start( [c5] )
    A.start( [c5] )
    B.start( [c5] )
    '''
    C.start( [c5] )
    D.start( [c5] )
    E.start( [c5] )
    F.start( [c5] )
    G.start( [c5] )
    '''

    sta1.cmd("arp -s 10.0.0.2 00:00:00:00:00:32 -i sta1-wlan0")
    sta1.cmd("arp -s 10.0.0.2 00:00:00:00:00:32 -i sta1-wlan1")
#    h2.cmd("arp -s 10.0.0.3 02:00:00:00:01:00")

    """uncomment to plot graph"""
#    net.plotGraph(max_x=160, max_y=160)

#    net.startMobility(startTime=0)
#    net.mobility(sta1, 'start', time=10, position='21.0,42.0,0.0')
#    net.mobility(sta1, 'start', time=10, position='12.0,48.0,0.0')
#    net.mobility(sta1, 'stop', time=25, position='74.0,48.0,0.0')
#    net.stopMobility(stopTime=50)

    print "***Exporting APs parameters"
    ap1_file = open("ap1.txt","w")
    ap1_file.write("{'delay': 15, 'jitter': 0, 'packet_loss': 0, 'av_bandwidth': 8}")
    ap1_file.close()
    ap2_file = open("ap2.txt","w")
    ap2_file.write("{'delay': 16, 'jitter': 10, 'packet_loss': 1.2, 'av_bandwidth': 42}")
    ap2_file.close()
    ap3_file = open("ap3.txt","w")
    ap3_file.write("{'delay': 11, 'jitter': 6, 'packet_loss': 2.8, 'av_bandwidth': 27}")
    ap3_file.close()
    ap4_file = open("ap4.txt","w")
    ap4_file.write("{'delay': 12, 'jitter': 7.0, 'packet_loss': 4.6, 'av_bandwidth': 31.0}")
    ap4_file.close()
    ap5_file = open("ap5.txt","w")
    ap5_file.write("{'delay': 13, 'jitter': 5, 'packet_loss': 1.6, 'av_bandwidth': 21}")
    ap5_file.close()
    ap6_file = open("ap6.txt","w")
    ap6_file.write("{'delay': 14, 'jitter': 11, 'packet_loss': 3.0, 'av_bandwidth': 39}")
    ap6_file.close()

    print "*** Running CLI"
    os.system("iw dev ap1-wlan1 interface add mon1 type monitor")
    os.system("ifconfig mon1 up")
#    os.system("python init_flow_add.py")
#    sta1.cmd("ufw enable &")
#    sta1.cmdPrint("tcpdump -i any -n -tt -v udp port 12346 > ~/exps/vid/rd_a01 &")
#    h2.cmdPrint("tcpdump -n -tt -v udp port 12346 > ~/exps/vid/sd_a01 &")
#    h2.cmdPrint("mp4trace -f -s 10.0.0.10 12346 ~/exps/vid/a01.mp4 > ~/exps/vid/st_a01 &")

#    h2.cmd("ping 10.0.0.10 &")
#    def read_last_lines():
#       ap1.cmd('./read_last_lines.py')

    def host_range():
      while getattr(t, "do_run", True):
       for host in net.hosts:
         if str(host)[0] == 's':
            x = host.params['ip'][0]
            x = x.replace("/8","")
            host_arc = open(x+"_scan.txt","w")
            aps = []
            for j in host.params['apsInRange']:
              aps.append(str(j))
#           host_arc.write(str(host.params['apsInRange']))
            host_arc.write(str(aps))         
            time.sleep(1)

    for host in net.hosts:
#       host = str(host)
       if str(host)[0] == 's':
          host.cmd('ping 10.0.0.2 &')
          host.cmd('./connection.sh &')


    ap1.cmd('./dbm.sh')
    t = threading.Thread(target=host_range)
#    t.daemon = True
    t.start()
    ap1.cmd('./read_last_lines.sh &')



#    ap1.cmd('./tcp_client.py &')

 #   for host in net.hosts:
#       host = str(host)
 #      if str(host)[0] == 's':
#          host.cmd('./ping_script.sh')

    
    CLI( net )

    print "*** Stopping network"
    net.stop()
    t.do_run = False
    
    response=open("response.txt","w")
    response.write(" ")
    response.close()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

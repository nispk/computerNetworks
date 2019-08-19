#!/usr/bin/python

"""This example shows how to work in adhoc mode

It is a full mesh network

     .sta3.
    .      .
   .        .
sta1 ----- sta2"""

import sys , math
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.node import Node, Host
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.propagationModels import propagationModel
import os, subprocess
import numpy as np


def topology(mobility):
    "Create a network."
    net = Mininet_wifi(link = wmediumd, wmediumd_mode = interference, controller= Controller)

    info("*** Creating nodes\n")
    if mobility:
        sta1 = net.addStation('sta1', recordNodeParams =True)
        sta2 = net.addStation('sta2', recordNodeParams =True)
        sta3 = net.addStation('sta3', recordNodeParams =True)
        sta4 = net.addStation('sta4', recordNodeParams =True)
        sta5 = net.addStation('sta5', recordNodeParams =True)

    else:
        sta1 = net.addStation('sta1', position='10,10,0', recordNodeParams =True)
        sta2 = net.addStation('sta2', position='40,20,0', recordNodeParams =True)
        sta3 = net.addStation('sta3', position='90,30,0', recordNodeParams =True)
        sta4 = net.addStation('sta4', position='50,40,1', recordNodeParams =True)
        sta5 = net.addStation('sta5', position='60,50,2', recordNodeParams =True)


    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4)


    def pathloss_logDistance(sta1,dist,wlan):
         """Path Loss Model:
         (f) signal frequency transmited(Hz)
         (d) is the distance between the transmitter and the receiver (m)
         (c) speed of light in vacuum (m)
         (L) System loss"""
         f = sta1.params['freq'][wlan] * 10 ** 9  # Convert Ghz to Hz
         c = 299792458.0
         L = 1
         if dist == 0:
             dist = 0.1
         lambda_ = c / f  # lambda: wavelength (m)
         denominator = lambda_ ** 2
         numerator = (4 * math.pi * dist) ** 2 * L
         pathLoss_ = 10 * math.log10(numerator / denominator)

         return pathLoss_

    def logDistance(sta1,sta2,exp):
         """Log Distance Propagation Loss Model:
         ref_d (m): The distance at which the reference loss is
         calculated
         exponent: The exponent of the Path Loss propagation model, where 2
         is for propagation in free space
         (dist) is the distance between the transmitter and the receiver (m)"""
         gr = sta1.params['antennaGain'][0]
         pt = sta2.params['txpower'][0]
         gt = sta2.params['antennaGain'][0]
         gains = pt + gt + gr
         ref_d = 1
         pl = pathloss_logDistance(sta1,ref_d,0)
         x = sta1.params['position']
         y = sta2.params['position']
         a = y[0]-x[0]
         b = y[1]-x[1]
         c = y[2]-x[2]
         d = math.sqrt((a**2)+(b**2)+(c**2))
         if d == 0:
             d = 0.1
         pldb = 10 * exp * math.log10(d / ref_d)
         rssi = gains - (int(pl) + int(pldb))

         return rssi

    nodes = [sta1,sta2,sta3,sta4,sta5]
    sta1_attn = [sta1]
    sta2_attn = [sta2]
    sta3_attn = [sta3]
    sta4_attn = [sta4]
    sta5_attn = [sta5]
    txpower = ['txpower',sta1.params['txpower'],sta2.params['txpower'],sta3.params['txpower'],sta4.params['txpower'],sta5.params['txpower']]

    for sta in nodes:
        for next in nodes:
            if(next != sta):
                new_rssi = logDistance(sta,next,exp=4)
                attn = sta.params['txpower'][0]-new_rssi
#                print('rssi between',sta,'and',next,'is',new_rssi)
                if(next == sta1):
                    sta1_attn.append(attn)
                elif (next == sta2):
                    sta2_attn.append(attn)
                elif (next == sta3):
                    sta3_attn.append(attn)
                elif(next == sta4):
                    sta4_attn.append(attn)
                else:
                    sta5_attn.append(attn)

    sta1_attn.insert(1,0)
    sta2_attn.insert(2,0)
    sta3_attn.insert(3,0)
    sta4_attn.insert(4,0)
    sta5_attn.insert(5,0)


#    print 'sta1 rx is',sta1_rx
#    print 'sta2 rx is',sta2_rx
    nodes.insert(0,'stations')
    np.savetxt('attenuation.csv',[p for p in zip(nodes,txpower,sta1_attn,sta2_attn,sta3_attn,sta4_attn,sta5_attn)], delimiter=',', fmt='%s')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(sta1, cls=adhoc, ssid='meshNet',
                channel=5, ht_cap='HT40+') #, passwd='thisisreallysecret')
    net.addLink(sta2, cls=adhoc, ssid='meshNet',
                channel=5, ht_cap='HT40+') #, passwd='thisisreallysecret')
    net.addLink(sta3, cls=adhoc, ssid='meshNet',
                channel=5, ht_cap='HT40+') #, passwd='thisisreallysecret')
    net.addLink(sta4, cls=adhoc, ssid='meshNet',
                channel=5, ht_cap='HT40+') #, passwd='thisisreallysecret')
    net.addLink(sta5, cls=adhoc, ssid='meshNet',
                channel=5, ht_cap='HT40+') #, passwd='thisisreallysecret')

    if mobility:
        net.plotGraph(max_x=100, max_y=100)
        net.startMobility(time=0, model='RandomDirection',
                          max_x=100, max_y=100,
                          min_v=0.5, max_v=0.8, seed=20)

    net.plotGraph(max_x=200, max_y=200)

    info("*** Starting network\n")
    net.build()


    info("*** Running CLI\n")
    cli = CLI_wifi(net)


    info("*** Stopping network\n")
    net.stop()

    #command = "sudo mn py sta1.params['txpower'] > /home/asn/txpower.dat"
    #sub = node1.popen(command, shell = True)

if __name__ == '__main__':
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)

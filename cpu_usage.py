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
import os.path
import numpy as np

#tl = Timeloop()

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

    nodes = [sta1,sta2,sta3,sta4,sta5]
    sta1_attn = [sta1]
    sta2_attn = [sta2]
    sta3_attn = [sta3]
    sta4_attn = [sta4]
    sta5_attn = [sta5]
    txpower = ['txpower',sta1.params['txpower'],sta2.params['txpower'],sta3.params['txpower'],sta4.params['txpower'],sta5.params['txpower']]

    ''''

    def attenuation_csv(self,nodes,counter,sta1_attn,sta2_attn,sta3_attn,sta4_attn,sta5_attn,txpower):
            while (counter<6):
                for sta in nodes:
                    for next in nodes:
                        if(next != sta):
                            print (type(next),type(sta))
                            attn = self.logDistance(sta,next,4)
                            if(next == nodes[0]):
                                sta1_attn.append(attn)
                            elif (next == nodes[1]):
                                sta2_attn.append(attn)
                            elif (next == nodes[2]):
                                sta3_attn.append(attn)
                            elif(next == nodes[3]):
                                sta4_attn.append(attn)
                            else:
                                sta5_attn.append(attn)
                sta1_attn.insert(1,0)
                sta2_attn.insert(2,0)
                sta3_attn.insert(3,0)
                sta4_attn.insert(4,0)
                sta5_attn.insert(5,0)
                nodes.insert(0,'stations')
                filename = "attenuation_" + str(counter) + ".csv"
                path = '/home/asn/'
                np.savetxt(filename,[p for p in zip(nodes,txpower,sta1_attn,sta2_attn,sta3_attn,sta4_attn,sta5_attn)], delimiter=',', fmt='%s')

                counter = counter + 1
    '''''




    net.attenuation_csv(nodes,1,sta1_attn,sta2_attn,sta3_attn,sta4_attn,sta5_attn,txpower)


    def get_processing_capacity(sta):
        available_capacity = sta.cmd('top -b -d1 -n1|grep -i "Cpu(s)"|cut -c 37-40')

        #command = 'top -b -d1 -n1|grep -i "Cpu(s)"|cut -c 37-40'
        #sub = subprocess.Popen([command], shell = True, preexec_fn=os.setsid)


    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)
    #tl.start(block = True)

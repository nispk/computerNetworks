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
from mininet.link import TCIntf
from mn_wifi.link import wmediumd, mesh, adhoc
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import CPULimitedStation
from mininet.topolib import TreeTopo
from mininet.util import custom, quietRun
from mn_wifi.wmediumdConnector import interference
from mn_wifi.propagationModels import propagationModel
import os, subprocess
import os.path
import numpy as np




def runProcSta(cpu, duration=5):

    pids = {}
    for s in stations:
        pids[s] = []
        for _core in range(num_procs):
            s.cmd('while true; do a=1; done &')
            pids[s].append(s.cmd('echo $!').strip())
        print ('the pid in station %s',pids[s],s)
    outputs = {}
    for s, pids in pids.items():
        for pid in pids:
            s.cmd('kill -9 %s' % pid)
    



def topology(mobility, bw =10, cpu = 0.2):
    "Create a network."
    """Example/test of link and CPU bandwidth limits
           bw: interface bandwidth limit in Mbps
           cpu: cpu limit as fraction of overall CPU time"""
        #intf = custom( TCIntf, bw=bw )
        #myTopo = TreeTopo( depth=1, fanout=2 )
    '''
    for sched in 'rt', 'cfs':
            info( '*** Testing with', sched, 'bandwidth limiting\n' )
            if sched == 'rt':
                release = quietRun( 'uname -r' ).strip('\r\n')
                output = quietRun( 'grep CONFIG_RT_GROUP_SCHED /boot/config-%s'
                                   % release )
                if output == '# CONFIG_RT_GROUP_SCHED is not set\n':
                    info( '*** RT Scheduler is not enabled in your kernel. '
                          'Skipping this test\n' )
                    continue
            Station = custom(CPULimitedStation, sched=sched, cpu=0.2)
            #net = Mininet( topo=myTopo, intf=intf, host=host ) '''

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

    #testLinkLimit( net, bw=bw )
    net.get_cpu_usage(duration=5)

    info("*** Running CLI\n")
    cli = CLI_wifi(net)
    #net.attenuation_csv(nodes,1)


    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)
    #tl.start(block = True)

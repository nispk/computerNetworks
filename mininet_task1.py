#!/usr/bin/python

"""This example shows how to work in adhoc mode

It is a full mesh network

     .sta3.
    .      .
   .        .
sta1 ----- sta2"""


import sys , math
from mininet.node import Controller
from mininet.log import setLogLevel, info, output
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
from time import sleep
import os, subprocess
import os.path
import numpy as np
import pandas as pd


def pathloss_logDistance(sta,dist,wlan):
         """Path Loss Model:
         (f) signal frequency transmited(Hz)
         (d) is the distance between the transmitter and the receiver (m)
         (c) speed of light in vacuum (m)
         (L) System loss"""
         f = sta.params['freq'][wlan] * 10 ** 9  # Convert Ghz to Hz
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
         attn = sta1.params['txpower'][0]-rssi
         return attn

def attenuation_csv(stations,counter,mobility):
    attn = 0

    if mobility:
        counter = counter
    else:
        counter = 6
    while (counter<=6):
        sta_attn = {keys: [] for keys in stations}
        for src in stations:
            for dst in stations:
                if(src == dst):
                    sta_attn[src].append(0)
                else:
                    attn = logDistance(src,dst,4)
                    sta_attn[src].append(attn)
        export_data = {'stations':stations}
        for i in stations:
            export_data[str(i.params['ip'])]= sta_attn[i]
        filename = 'attenuation_'+str(counter)+'.csv'
        df = pd.DataFrame(export_data, columns=[str(i.params['ip']) for i in stations])

        df.to_csv(filename, index=None, header=True)
        print('export to csv')
        counter = counter + 1

#tl = Timeloop()
def testLinkLimit(net, bw):
    "Run bandwidth limit test"
    info( '*** Testing network %.2f Mbps bandwidth limit\n' % bw )
    net.iperf()


def get_cpu_usage(stations,duration=1,count=1):
    """run CPU limit test with 'while true' processes.
    cpu: desired CPU fraction of each host
    duration: test duration in seconds (integer)
    returns a single list of measured CPU fractions as floats.
    """
    #pid = startProcSta(stations) #start a process on stations to create cpuacct file
    

    outputs = {}
    time = {}
    t_start = {}

    for station in stations:
        ip = station.params['ip']
        outputs[str(ip)] = []
        with open('/sys/fs/cgroup/cpuacct/%s/cpuacct.usage'
                  % station, 'r') as f:
            time[station] = float(f.read())
        t_start[station] = station.cmd('date +%s%N')

    for _ in range(count): # count decides number of screenshots of cpu_usage for each station to be taken.
        sleep(duration)
        for station in stations:
            ip = station.params['ip']
            with open('/sys/fs/cgroup/cpuacct/%s/cpuacct.usage'
                      % station, 'r') as f:
                readTime = float(f.read())
            t_stop = station.cmd('date +%s%N')
            outputs[str(ip)].append(((readTime - time[station])
                                  / (int(t_stop)-int(t_start[station])))*100)

            time[station] = readTime
            t_start[station] = station.cmd('date +%s%N')

    filename = 'cpu_usage.csv'
    df = pd.DataFrame(outputs, columns=[str(i.params['ip']) for i in stations])

    df.to_csv(filename, index=None, header=True)
    print('data exported')

    output('*** Results: %s\n' % outputs)
    #return outputs



def topology(mobility):
    "Create a network."

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
            Station = custom(CPULimitedStation, sched=sched, cpu=0.5)  #cpu: cpu limit as fraction of overall CPU time. each station assigned cpu limit using CPULimitedStation class


    net = Mininet_wifi(link = wmediumd, wmediumd_mode = interference, controller= Controller, station = Station)


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

    stations = [sta1,sta2,sta3,sta4,sta5]



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
    get_cpu_usage(stations,duration=5,count=5)

    if mobility:
        attenuation_csv(stations,1,1)
    else:
        attenuation_csv(stations,1,0)

    info("*** Running CLI\n")
    cli = CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()




if __name__ == '__main__':
    setLogLevel('info')
    mobility = True if '-m' in sys.argv else False
    topology(mobility)
    #tl.start(block = True)

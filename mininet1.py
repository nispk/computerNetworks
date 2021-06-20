import sys, os
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import Intf, Link

def Simple_topology():
    net = Mininet(link = Link, intf = Intf)
    # Creating nodes
    sta1 = net.addHost('sta1')
    sta2 = net.addHost('sta2')
    sta3 = net.addHost('sta3')
    sta4 = net.addHost('sta4')

    # Creating links
    net.addLink(sta1, sta2)
    net.addLink(sta2, sta3)
    net.addLink(sta3, sta4)

    #Start network
    net.build()
  
    # Runn CLI\n'
    CLI(net)

    info('*** Stop network\n')
    net.stop()

if __name__== '__main__':
    Simple_topology()


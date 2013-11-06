#!/usr/bin/python

"""
"""
import sys
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

Switch = OVSKernelSwitch

def routerNet():
    "Create a network with a router and two switches"
    c = RemoteController
    net = Mininet( controller=c, switch=Switch, autoSetMacs=True, autoStaticArp=True)

    print "*** Creating controller"
    if len(sys.argv) > 1:
        print sys.argv[0]
        c1 = net.addController( 'c1', port=6633, ip=sys.argv[1] )
    else:
        c1 = net.addController( 'c1', port=6633 )

    print "*** Creating switches"
    s1 = net.addSwitch('s1', dpid='0000000000000101')
    s2 = net.addSwitch('s2', dpid='0000000000000201')
    r1 = net.addSwitch('r1', dpid='0000000000000001')

    print "*** Creating hosts"
    h1 = net.addHost('h1', ip='10.0.1.2/24', mac='00:00:00:00:01:02')
    h2 = net.addHost('h2', ip='10.0.2.2/24', mac='00:00:00:00:02:02')

    print "*** Creating links"
    net.addLink(h1,s1)
    net.addLink(h2,s2)
    net.addLink(s1,r1)
    net.addLink(s2,r1)

    print "*** Starting network"
    net.start()
    net.getNodeByName('h1').cmd('route add -net 10.0.2.0 netmask 255.255.255.0 gw 10.0.1.1')
    net.getNodeByName('h1').cmd('arp -s 10.0.1.1 00:00:00:00:01:01')
    net.getNodeByName('h2').cmd('route add -net 10.0.1.0 netmask 255.255.255.0 gw 10.0.2.1')
    net.getNodeByName('h2').cmd('arp -s 10.0.2.1 00:00:00:00:02:01')

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    routerNet()

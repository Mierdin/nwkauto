import sys
import os

from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
from jnpr.junos.op.lldp import LLDPNeighborTable
from jnpr.junos.op.routes import RouteTable

dev = Device(
    host='127.0.0.1', user='root', password='Juniper', port=sys.argv[1]
)

dev.open()

# Warning - this will break if you haven't applied the base configuration yet

lldpneis = LLDPNeighborTable(dev).get()

print("LLDP Neighbors: %s" % len(lldpneis))

scriptdir = os.path.dirname(os.path.realpath(__file__))

globals().update(loadyaml('%s/bgpneighbor.yml' % scriptdir))

bgpneighbors = BGPNeighborTable(dev).get()

print("BGP Neighbors: %s" % len(bgpneighbors))

route_table = RouteTable(dev)
routes = route_table.get('123.123.123.1/24')
if len(routes) == 1:
    print("Mission ACCOMPLISHED")
else:
    print("Mission NOT YET ACCOMPLISHED")

dev.close()

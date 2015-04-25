from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.op.lldp import LLDPNeighborTable

# Need to check vagrant ssh-config to ensure correct port
dev = Device(host='127.0.0.1', user='root', password='Juniper', port=<port>)
dev.open()

pprint(dev.facts)

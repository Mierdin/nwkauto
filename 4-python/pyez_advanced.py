from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
from jnpr.junos.op.lldp import LLDPNeighborTable
from jnpr.junos.exception import ConnectRefusedError

# Dictionary to hold our devices. Key is the device name, and the
# value for each key is the corresponding Device object used to
# connect to the vSRX
devs = {}

# Don't forget to check vagrant ssh-config!
# Dictionary for easy matching of name to SSH port
portmapping = {
    'vsrx01': '2222',
    'vsrx02': '2200',
    'vsrx03': '2201'
}

# Add device objects to dictionary
for devname, devport in portmapping.items():
    devs[devname] = Device(
        host='127.0.0.1', user='root', password='Juniper', port=devport
    )

print("------FACTS------")

# Connect to each of our devices, and print out basic facts
# Doesn't take much to get this - received automatically when connecting
for devname, device in devs.items():

    try:
        device.open()
    except ConnectRefusedError:
        pass  # Don't care, c'est la vie!

    pprint(device.facts)

print("------LLDP------")

# Some advanced info requires Tables
# Tables are a PyEZ construct for retrieving
# more detailed information than basic facts.
# LLDPNeighborTable is built in to the library

# Loop through devices
for devname, device in devs.items():

    # Proper introductions
    print("Hi! I'm %s!" % devname)

    # Retrieve LLDP neighbors
    lldpneis = LLDPNeighborTable(device).get()

    # Loop over LLDP neighbors for this device
    for lldpnei in lldpneis:
        print('I see that %s is connected to my %s interface.' % (
            lldpnei.remote_sysname, lldpnei.key
            )
        )

print("------BGP------")

# If your table is not built in to PyEZ, you can build your own!
# See bgpneighbor.yml, referenced below
# Also look at the "display xml [rpc] JunOS command"
globals().update(loadyaml('bgpneighbor.yml'))

# Loop over devices
for devname, device in devs.items():

    # Proper introductions
    print("Hi! I'm %s!" % devname)

    # Retrieve BGP Neighbors
    bgpneighbors = BGPNeighborTable(device).get()

    # Loop over BGP neighbors for this device
    for bgpnei in bgpneighbors:

        print('My BGP neighbor: %s from AS# %s has sent me %s prefixes.' % (
            bgpnei.peeraddr,
            bgpnei.peeras,
            bgpnei.pfx_rx
            )
        )

# Clean up!
for devname, device in devs.items():
    device.close()

from ncclient import manager

host = '127.0.0.1'
user = 'root'
password = 'Juniper'
port = 2200

with manager.connect(host=host,
                     port=port,
                     username=user,
                     hostkey_verify=False,
                     password=password,
                     device_params={'name': 'junos'}) as m:
    print m.dispatch('get-lldp-neighbors-information')
    # Dispatch an RPC command yourself (obviously vendor-specific)


from pprint import pprint
from jnpr.junos import Device

dev = Device(host='10.12.0.77', user='root', password='Password1!')
dev.open()

pprint(dev.facts)

dev.close()

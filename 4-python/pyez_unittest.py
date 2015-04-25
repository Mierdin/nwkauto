from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable
from jnpr.junos.factory import loadyaml
import unittest


class RoutingTestSuite(unittest.TestCase):

    def setUp(self):
        self.dev = Device(
            host='127.0.0.1', user='root', password='Juniper', port='2222'
        )
        self.dev.open()

    def tearDown(self):
        self.dev.close()


class GetRouteTest(RoutingTestSuite):

    def runTest(self):

        route_table = RouteTable(self.dev)

        routes = route_table.get('123.123.123.1/24')

        # Checks for a single route recieved via BGP. Uncomment to enable
        self.assertEqual(len(routes), 1)


class GetBgpNeighborsTest(RoutingTestSuite):

    def runTest(self):
        globals().update(loadyaml('bgpneighbor.yml'))

        bgpneighbors = BGPNeighborTable(self.dev).get()

        for bgpnei in bgpneighbors:
            self.assertEqual(int(bgpnei.pfx_rx), 1)

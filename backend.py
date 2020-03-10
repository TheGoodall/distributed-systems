
import Pyro4
print("Starting backend")
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class backend(object):
    def __init__(self):
        self.orders = []
    def make_order(self, order, address):
        print("New order: {0}".format(order))
        self.orders.append(order)
        return self.orders
    def get_orders(self):
        return self.orders
    def update_orders(self, orders):
        self.orders = orders


daemon = Pyro4.Daemon()
uri = daemon.register(backend)

backend_management = Pyro4.Proxy("PYRONAME:FE.backend_management")

name = backend_management.get_name()

ns= Pyro4.locateNS()
ns.register(name, uri)
daemon.requestLoop()


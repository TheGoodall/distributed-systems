
import Pyro4
print("Starting backend")
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class backend(object):
    def __init__(self):
        self.orders = []
        self.backend_manager = Pyro4.Proxy("PYRONAME:FE.backend_manager")
    def make_order(self, order, address):
        print("New order: {0}".format(order))
        self.orders.append(order)
        for backend in self.backend_manager.get_non_primary_backends():
            try:
                backend[1].make_order(order, address)
            except Pyro4.errors.CommunicationError:
                self.backend_manager.demote_backend(backend[0])
        return self.orders
    def get_orders(self):
        return self.orders
    def update_orders(self, orders):
        self.orders = orders


daemon = Pyro4.Daemon()
uri = daemon.register(backend)

backend_manager = Pyro4.Proxy("PYRONAME:FE.backend_manager")

name = backend_manager.get_name()

ns= Pyro4.locateNS()
ns.register(name, uri)


daemon.requestLoop()


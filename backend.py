import Pyro4
print("Starting backend")
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class backend(object):
    def __init__(self):
        self.backend_manager = Pyro4.Proxy("PYRONAME:FE.backend_manager")
        self.orders = []
    def update_orders_from_primary(self):
        primary = self.backend_manager.get_backend()
        
        if primary == []:
            self.orders = []
        else:
            self.orders = primary[1].get_orders()

    def make_order(self, order, postcode):
        self.orders.append([order, postcode])
        for backend in self.backend_manager.get_non_primary_backends():
            try:
                backend[1].update_orders_from_primary()
            except Pyro4.errors.CommunicationError:
                self.backend_manager.demote_backend(backend[0])
    
        return self.orders
    def set_order(self, order, postcode):
        self.orders.append([order, postcode])
        return self.orders

    def get_orders(self):
        return self.orders
    def update_orders(self, orders):
        self.orders = orders


daemon = Pyro4.Daemon()
uri = daemon.register(backend)

backend_manager = Pyro4.Proxy("PYRONAME:FE.backend_manager")

name = backend_manager.get_name()
print("Name: {0}".format(name))
ns= Pyro4.locateNS()
ns.register(name, uri)


daemon.requestLoop()


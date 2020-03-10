
import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class backend(object):
    def __init__(self):
        self.orders = []
    def make_order(self, order, address):
        print("Making Order")
        self.orders.append(order)
        success = True
        return success
    def get_orders(self):
        return self.orders


daemon = Pyro4.Daemon()
uri = daemon.register(backend)

ns= Pyro4.locateNS()
ns.register("1.backend", uri)
daemon.requestLoop()


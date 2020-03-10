
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

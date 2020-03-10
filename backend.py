
import Pyro4

@Pyro4.expose
class backend(object):
    def make_order(self, order, address):
        print("Making Order")
        success = True
        return success

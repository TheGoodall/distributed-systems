print("Starting Frontend")
import Pyro4
primary = 0
backends = []

backends.append(["PYRONAME:1.backend", Pyro4.Proxy("PYRONAME:1.backend")])

@Pyro4.expose
class backend_management(object):
    def register_new_backend(self, uri):
        print("New Backend: {0}".format(uri))
        backends.append([uri, Pyro4.Proxy(uri)])
    def delete_backend(self, uri):
        backends = filter(lambda x: not(uri != x[0]), backends)
    def is_registered(self, uri):
        return uri in map(lambda x: x[0] ,backends)
    def get_name(self):
        i=1
        while "{0}.backend".format(i) in map(lambda x: x[0], backends):
            i+=1
        return "{0}.backend".format(i)


@Pyro4.expose
class order_management(object):
    def address_from_postcode(self, postcode):
        return postcode
    def new_order(self, order, postcode):
        backends[primary][1].make_order(order, self.address_from_postcode(postcode))
    



daemon = Pyro4.Daemon()
uri_backend_management = daemon.register(backend_management)
uri_order_management = daemon.register(order_management)

ns= Pyro4.locateNS()
ns.register("FE.order_management", uri_order_management)
ns.register("FE.backend_management", uri_backend_management)

daemon.requestLoop()

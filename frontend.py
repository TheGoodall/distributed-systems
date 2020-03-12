print("Starting Frontend")
import Pyro4
primary = 0
backends = []

backends.append(["PYRONAME:1.backend", Pyro4.Proxy("PYRONAME:1.backend")])

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class backend_manager(object):
    def __init__(self):
        self.backends = []

    def register_new_backend(self, uri):
        self.backends.append([uri])
    def is_registered(self, uri):
        return uri in map(lambda x: x[0] ,self.backends)
    def get_name(self):
        print("Getting name, backends currently {0}".format(self.backends))
        print("")
        i=1
        while "PYRONAME:{0}.backend".format(i) in map(lambda x: x[0], self.backends):
            i+=1
        self.backends.append(["PYRONAME:{0}.backend".format(i)])
        print("New Backend: {0}".format(i))
        return "{0}.backend".format(i)
    

    def get_non_primary_backends(self):
        backends = []
        for i in range(1, len(self.backends)):
            backends.append(self.get_backend(i))
        return backends


    # Order manager
    
    def demote_backend(self, uri):
        print("Demoting backend: {0}\n current backends are: {1}".format(uri, self.backends))
        self.backends = [backend for backend in self.backends if backend[0] != uri].append([uri])
        if self.backends == None:
            self.backends = []
        print("Backends after demotion are: {0}".format(self.backends))


    def get_backend(self, n=0):
        if len(self.backends) == 0:
            return []
        if len(self.backends[n]) == 2:
            return self.backends[n]
        else:
            self.backends[n].append(Pyro4.Proxy(self.backends[n][0]))
            return self.backends[n]
    
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class order_manager(object):
    def __init__(self):
            self.backend_manager = Pyro4.Proxy("PYRONAME:FE.backend_manager")
    def address_from_postcode(self, postcode):
        return postcode
    def new_order(self, order, postcode):
        while 1:
            try:
                backend = self.backend_manager.get_backend()
                if backend == []:
                    return False
                backend[1].make_order(order, self.address_from_postcode(postcode))
            except Pyro4.errors.CommunicationError as error:

                self.backend_manager.demote_backend(backend[0])

            else:
                break
        return True

    


daemon = Pyro4.Daemon()
uri_backend_manager = daemon.register(backend_manager)
uri_order_manager = daemon.register(order_manager)

ns= Pyro4.locateNS()
ns.register("FE.order_manager", uri_order_manager)
ns.register("FE.backend_manager", uri_backend_manager)

daemon.requestLoop()

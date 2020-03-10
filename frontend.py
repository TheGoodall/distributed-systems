
import Pyro4

backend = Pyro4.Proxy("PYRONAME:1.backend")

print(backend.get_orders())
print(backend.make_order("", ""))


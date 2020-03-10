import Pyro4

FE = Pyro4.Proxy("PYRONAME:FE.order_management")

FE.new_order("new order", "BB7 9PZ")


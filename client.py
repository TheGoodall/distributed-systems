import Pyro4

FE = Pyro4.Proxy("PYRONAME:FE.order_manager")

while 1:
    print("What do you want to order?")
    order = input("> ")
    print("Where would you like it to be delivered to? (postcode)")
    address = input("> ")
    
    success = FE.new_order(order, address)
    if not success:
        print("Failed")


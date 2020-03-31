import Pyro4

FE = Pyro4.Proxy("PYRONAME:FE.order_manager")

while 1:
    print("Do you want to make a (N)ew order or to (V)iew orders already placed, or (E)xit?")
    selection = input("> ")
    if selection == "N":
        print("What do you want to order?")
        order = input("> ")
        print("Where would you like it to be delivered to? (postcode)")
        address = input("> ")
        
        success = FE.new_order(order, address)
        if not success:
            print("ERROR, Could not add order!")
    elif selection == "V":
        orders = FE.get_orders()
        if orders == False:
            print("ERROR, could not get orders")
            continue
        for order in orders:
            print("\n{0}\nOrdered to: {1}".format(order[0], order[1]))
    elif selection == "E":
        exit(0)
    else:
        print("INVALID SELECTION!")

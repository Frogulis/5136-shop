import Order
import Product


class Store:
    def __init__(self, products, customers, owner, orderHistory):
        self.products = products
        self.customers = customers
        self.owner = owner
        self.orderHistory = orderHistory

    def getProducts(self):
        return self.products;

    def setProducts(self, productList):
        self.products = productList

    def getCustomers(self):
        return self.customers

    def setCustomers(self, customerList):
        self.customers = customerList

    def getOwner(self):
        return self.owner

    def setOwner(self, ownerLoggedIn):
        self.owner = ownerLoggedIn

    def getOrderHistory(self):
        return self.orderHistory

    def setOrderHistory(self, allOrders):
        self.orderHistory = allOrders

    def getParticularOrder(self, orderID):
        orders = self.getOrders()
        return orders[orderID]

    def getOrders(self):
        return Order()

    def searchProduct(self, productID):
        products = self.getProduct()
        product = products[productID]

    def getProduct(self):
        return Product()


if __name__ == '__main__':
    # put parameters to create Store object
    products = ["Apple", "Banana", "Orange"]
    customers = ["C1000", "C1001", "C1002", "C1003"]
    owner = "O1500"
    orderHistory = [{"C1000": "Order1"}, {"C1002": "Order2"}]

    # create object
    c = Store(products, customers, owner, orderHistory)

    print (c.getParticularOrder('Order3'));
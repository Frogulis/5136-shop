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

    def editProduct(self, productID):
        product = [{'ProductID': '1', 'ProductName': 'Apples', 'Unit': 'kg', 'originalPrice': 3.99
                    , 'Source': 'unknown', 'ShelfLife': 7,
                   'Batches': [{'BatchId': 'Apples1', 'ExpiryDate': '15/10/18', 'Quantity': 5}]}
            , {'ProductID': '2', 'ProductName': 'Bananas', 'Unit': 'kg', 'originalPrice': 3.99
                    , 'Source': 'unknown', 'ShelfLife': 7,
                   'Batches': [{'BatchId': 'Apples1', 'ExpiryDate': '15/10/18', 'Quantity': 5}]}
            , {'ProductID': '3', 'ProductName': 'Strawberries', 'Unit': 'kg', 'originalPrice': 3.99
                    , 'Source': 'unknown', 'ShelfLife': 7,
                   'Batches': [{'BatchId': 'Apples1', 'ExpiryDate': '15/10/18', 'Quantity': 5}]}
            , {'ProductID': '4', 'ProductName': 'Apples (bag)', 'Unit': 'ea', 'originalPrice': 3.99
                    , 'Source': 'unknown', 'ShelfLife': 7,
                   'Batches': [{'BatchId': 'Apples1', 'ExpiryDate': '15/10/18', 'Quantity': 5}]}
            , {'ProductID': '5', 'ProductName': 'Kiwi', 'Unit': 'kg', 'originalPrice': 3.99
                    , 'Source': 'unknown', 'ShelfLife': 7,
                   'Batches': [{'BatchId': 'Apples1', 'ExpiryDate': '15/10/18', 'Quantity': 5}]}]


if __name__ == '__main__':
    products = ["Apple", "Banana", "Orange"]
    customers = ["C1000", "C1001", "C1002", "C1003"]
    owner = "O1500"
    orderHistory = [{"C1000": "Order1"}, {"C1002": "Order2"}]

    c = Store(products, customers, owner, orderHistory)

    print (c.getParticularOrder('Order3'));
import Order
from Product import Product
from CustomerAccount import CustomerAccount

import datetime


class Store:
    def __init__(self):
        # readfile()
        self.products = []
        self.customers = []
        self.owner = []
        self.orderHistory = {}

    def addProduct(self, name, unit, originalPrice, source, shelfLife):
        id = self.generateNewProductId()
        newProduct = Product(id, name, unit, originalPrice, source, shelfLife)
        self.products.append(newProduct)

    def addCustomer(self, password, name, phoneNum, address):
        id = self.generateNewCustomerId()
        newCustomer = CustomerAccount(id, password, name, phoneNum, address)
        self.customers.append(newCustomer)

    def generateNewCustomerId(self):
        if len(self.customers) == 0:
            return str(1)
        return str(int(self.customers[-1].getId())+1)


    def editProductName(self, productId, newName):
        productToBeEdited = self.getProduct(productId)
        productToBeEdited.setName(newName)

    def editProductUnit(self, productId, newUnit):
        productToBeEdited = self.getProduct(productId)
        productToBeEdited.setUnit(newUnit)

    def editProductOriginalPrice(self, productId, newPrice):
        productToBeEdited = self.getProduct(productId)
        productToBeEdited.setOriginalPrice(newPrice)

    def editProductSource(self, productId, newSource):
        productToBeEdited = self.getProduct(productId)
        productToBeEdited.setSource(newSource)

    def editProductShelfLife(self, productId, newShelfLife):
        productToBeEdited = self.getProduct(productId)
        productToBeEdited.setShelfLife(newShelfLife)

    # Please make sure the current user is the owner, validation needed.
    def getExpiredProducts(self):
        expiredProducts = []
        for product in self.products:
            for batch in product.getBatches():
                if batch.getExpiryDate() < datetime.datetime.now().date():
                    expiredProducts.append(batch)
        return expiredProducts

    def generateNewProductId(self):
        if len(self.products) == 0:
            return str(1)
        return str(int(self.products[-1].getId())+1)

    def getProduct(self, productId):
        for product in self.products:
            if product.getId() == productId:
                return product
        raise Exception("Product does not exist.")


    def getProducts(self):
        return self.products

    def setProducts(self, productList):
        self.products = productList

    def getCustomer(self, customerId):
        for customer in self.customers:
            if customer.getId() == customerId:
                return customer
        raise Exception("Customer does not exist.")

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

    def getParticularOrder(self, customerId, orderId):
        orders = self.orderHistory[customerId]
        for order in orders:
            if order.getOrderId() == orderId:
                return order
        raise Exception("Order does not exist.")


    def searchProductByName(self, keyword):  # TODO
        keyword.lower()
        matchingProducts = []
        for product in self.products:
            searchingProductName = product.getName().lower()
            if keyword in searchingProductName:
                matchingProducts.append(product)
        return matchingProducts

    def removeProduct(self, productId):
        try:
            productToBeRemoved = self.getProduct(productId)
            productIndex = self.products.index(productToBeRemoved)
            del self.products[productIndex]
        except Exception:
            raise Exception("Failed to remove product.")

    def removeCustomer(self, customerId):
        try:
            customerToBeRemoved = self.getCustomer(customerId)
            customerIndex = self.customers.index(customerToBeRemoved)
            del self.customers[customerIndex]
        except Exception:
            raise Exception("Failed to remove customer.")


if __name__ == '__main__':
    # put parameters to create Store object
    products = ["Apple", "Banana", "Orange"]
    customers = ["C1000", "C1001", "C1002", "C1003"]
    owner = "O1500"
    orderHistory = [{"C1000": "Order1"}, {"C1002": "Order2"}]

    # create object
    # c = Store(products, customers, owner, orderHistory)

    s=Store()
    s.addProduct('apple', 'bag', 2.5, 'china', 9)
    print(1, s.getProducts()[0].getId())
    s.editProductName('1', 'banana')
    s.editProductOriginalPrice('1','er')

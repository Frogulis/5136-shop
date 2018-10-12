from Order import Order
from Product import Product
from CustomerAccount import CustomerAccount
from OwnerAccount import OwnerAccount
from ShoppingCart import ShoppingCart

import datetime
import json
from pathlib import Path


class Store:
    def __init__(self):
        # readfile()
        self.products = []
        self.customers = []
        self.owner = OwnerAccount('owner', 'owner', 'owner')
        self.orderHistory = {}
        if Path("testbyyuki.json").is_file():
            self.readStore()

    def readStore(self):  # yuki
        with open('testbyyuki.json','r') as infile:
            savedStore = json.loads(infile.read())
        for productData in savedStore['products']:
            productId = productData['id']
            productName = productData['name']
            productUnit = productData['unit']
            productOriginalPrice = productData['originalPrice']
            productSource = productData['source']
            productShelfLife = productData['shelfLife']
            batches = productData['batch']
            product = Product(productId, productName, productUnit, productOriginalPrice, productSource, productShelfLife)
            for batch in batches:
                sDate = batch['shelfDate'].split('-')
                bShelfDate = datetime.date(int(sDate[0]), int(sDate[1]), int(sDate[2]))
                batchId = batch['batchId']
                batchActualPrice = batch['actualPrice']
                batchQuantity = batch['quantity']
                batchShelfDate = bShelfDate
                product.buildBatch(batchId, batchActualPrice, batchQuantity, batchShelfDate, productShelfLife)
            self.products.append(product)
        for customerData in savedStore['customers']:
            cId = customerData['id']
            cPassword = customerData['password']
            cName = customerData['name']
            cPhoneNumber= customerData['phoneNumber']
            cAddress = customerData['address']
            cBalance = customerData['balance']
            cShoppingCart = customerData['shoppingCart']
            customer = CustomerAccount(cId, cPassword, cName, cPhoneNumber, cAddress, cBalance)
            customer.shoppingCart.setProductsInCart(cShoppingCart)
            self.customers.append(customer)

        for customerId in savedStore['orderHistory']:
            cOrderList = savedStore['orderHistory'][customerId]
            customerOrders = []
            for eachOrder in cOrderList:
                orderId = eachOrder['orderId']
                orderCId = eachOrder['customerId']
                tempShoppingCart = eachOrder['shoppingCart']
                orderShoppingCart = ShoppingCart()
                orderShoppingCart.setProductsInCart(tempShoppingCart)
                orderTotalPrice = eachOrder['totalPrice']
                dateS = eachOrder['transactionDate'].split('-')
                orderTransactionDate = datetime.datetime(int(dateS[0]), int(dateS[1]), int(dateS[2]), int(dateS[3]), int(dateS[4]), int(dateS[5]))
                order = Order(orderId, orderCId, orderShoppingCart, orderTotalPrice, orderTransactionDate)
                customerOrders.append(order)
            self.orderHistory[customerId] = customerOrders

        ownerData = savedStore['owner']
        self.owner = OwnerAccount(ownerData['id'], ownerData['name'], ownerData['password'])

    def writeStore(self):  # yuki
        currStore = {'products': [],
                     'customers': [],
                     'owner': [],
                     'orderHistory': {}}
        for product in self.products:  # write product
            productData = {'id': product.getId(),
                           'name': product.getName(),
                           'unit': product.getUnit(),
                           'originalPrice': product.getOriginalPrice(),
                           'source': product.getSource(),
                           'shelfLife': product.getShelfLife(),
                           }
            batchList = []
            for batch in product.getBatches():
                batchData = {'batchId': batch.getBatchID(),
                             'shelfDate': batch.getShelfDate().strftime("%Y-%m-%d"),
                             'expiryDate': batch.getExpiryDate().strftime("%Y-%m-%d"),
                             'actualPrice': batch.getActualPrice(),
                             'quantity': batch.getQuantity()}
                batchList.append(batchData)
            productData['batch'] = batchList
            currStore['products'].append(productData)
        for customer in self.customers:  # write customer
            customerData = {'id': customer.getId(),
                            'password': customer.getPassword(),
                            'name': customer.getName(),
                            'phoneNumber': customer.getPhoneNumber(),
                            'address': customer.getAddress(),
                            'shoppingCart': customer.getShoppingCart().productsInCart,
                            'balance': customer.getBalance()}
            currStore['customers'].append(customerData)

        currStore['owner'] = {'id': self.owner.getId(),
                              'password': self.owner.getPassword(),
                              'name': self.owner.getName()}
        for customerId in self.orderHistory:
            orderList = self.orderHistory[customerId]
            ordersOfCustomer = []
            for order in orderList:
                orderData = {'orderId': order.getOrderId(),
                             'customerId': order.getCustomerId(),
                             'shoppingCart': order.getShoppingCart().productsInCart,
                             'totalPrice': order.getTotalPrice(),
                             'transactionDate': order.getTransactionDate().strftime("%Y-%m-%d-%H-%M-%S")}
                ordersOfCustomer.append(orderData)
            currStore['orderHistory'][customerId] = ordersOfCustomer
        # write currstore into json
        with open('testbyyuki.json','w') as outfile:
            json.dump(currStore, outfile)

    def addProduct(self, name, unit, originalPrice, source, shelfLife):
        pid = self.generateNewProductId()
        newProduct = Product(pid, name, unit, originalPrice, source, shelfLife)
        self.products.append(newProduct)

    def addCustomer(self, password, name, phoneNum, address):
        cid = self.generateNewCustomerId()
        newCustomer = CustomerAccount(cid, password, name, phoneNum, address)
        self.customers.append(newCustomer)
        return newCustomer

    def addOrder(self, customerId, pInSc, tPrice=0.0, tDate=datetime.datetime.now()):
        if customerId not in self.orderHistory:
            self.orderHistory[customerId] = []
        nid = self.generateNewOrderId(customerId)
        scRec = ShoppingCart()
        scRec.setProductsInCart(pInSc)
        newOrder = Order(nid, customerId, scRec, tPrice, tDate)
        self.orderHistory[customerId].append(newOrder)
        return newOrder

    def generateNewCustomerId(self):
        if len(self.customers) == 0:
            return str(1)
        return str(int(self.customers[-1].getId())+1)

    def generateNewOrderId(self, cid):
        if len(self.orderHistory[cid]) == 0:
            return str(1)
        else:
            return str(int(self.orderHistory[cid][-1].getOrderId()) + 1)

    def editCustomerName(self, customerId, newName):
        customerToBeEdit = self.getCustomer(customerId)
        customerToBeEdit.setName(newName)

    def editCustomerPassword(self, customerId, newPassWord):
        customerToBeEdit = self.getCustomer(customerId)
        customerToBeEdit.setPassword(newPassWord)

    def editCustomerPhoneNumber(self, customerId, newPhoneNumber):
        customerToBeEdit = self.getCustomer(customerId)
        customerToBeEdit.setPhoneNumber(newPhoneNumber)

    def editCustomerAddress(self, customerId, newAddress):
        customerToBeEdit = self.getCustomer(customerId)
        customerToBeEdit.setAddress(newAddress)

    def editCustomerBalance(self, customerId, newBalance):
        customerToBeEdit = self.getCustomer(customerId)
        customerToBeEdit.setBalance(newBalance)

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

    # All Order History as a whole list
    def getOrderHistoryAsList(self):
        orderHistoryList = []
        sortedKeys = sorted(self.orderHistory.keys())
        for key in sortedKeys:
            orderHistoryList.extend(self.orderHistory[key])
        return orderHistoryList

    def getCustomerOrders(self,customerId):
        if customerId in self.orderHistory:
            return self.orderHistory[customerId]
        else:
            return []        

    def getParticularOrder(self, customerId, orderId):
        orders = self.orderHistory[customerId]
        for order in orders:
            if order.getOrderId() == orderId:
                return order
        raise Exception("Order does not exist.")

    def searchProductByName(self, keyword):
        keyword = keyword.lower().strip()
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


    s = Store()

    """
    s.addCustomer('cs1','cs1','0450563312','add1')
    s.addCustomer('cs2','cs2','0450563312','add1')
    s.addCustomer('cs3','cs3','0450563312','add1')
    s.addProduct('apple','kg',5, 'China', 10)
    s.addProduct('banana', 'kg', 3, 'China', 5)
    s.getProduct('1').addBatch(20)
    s.getProduct('2').addBatch(30)
    #print(s.getProduct('2').getBatch('1').getExpiryDate().strftime("%Y-%m-%d"))
    #put product into shopping cart
    s.getCustomer('1').getShoppingCart().addToShoppingCart('1', 1.50, 4)
    s.getCustomer('1').getShoppingCart().addToShoppingCart('3', 3.89, 10)
    #print(s.getCustomer('1').getShoppingCart().productsInCart[:])
    c1sc = ShoppingCart()
    c1sc.setProductsInCart(s.getCustomer('1').getShoppingCart().productsInCart[:])
    #print(type(c1sc), c1sc.getTotalPrice())
    s.getCustomer('2').getShoppingCart().addToShoppingCart('2', 3.9, 13)
    s.getCustomer('2').getShoppingCart().addToShoppingCart('4', 3.89, 1)
    c2sc = ShoppingCart()
    c2sc.setProductsInCart(s.getCustomer('2').getShoppingCart().productsInCart[:])
    #c2sc = s.getCustomer('2').getShoppingCart()
    #addOrder
    s.addOrder('1', c1sc, c1sc.getTotalPrice())
    s.addOrder('2', c2sc, c2sc.getTotalPrice())
    s.getCustomer('2').getShoppingCart().addToShoppingCart('3', 3.89, 10)
    c2sc = ShoppingCart()
    c2sc.setProductsInCart(s.getCustomer('2').getShoppingCart().productsInCart[:])
    #c2sc = s.getCustomer('2').getShoppingCart()
    s.addOrder('2', c2sc, c2sc.getTotalPrice())


    products = ["Apple", "Banana", "Orange"]
    customers = ["C1000", "C1001", "C1002", "C1003"]
    owner = "O1500"
    orderHistory = [{"C1000": "Order1"}, {"C1002": "Order2"}]


    s.addProduct('apple', 'bag', 2.5, 'china', 9)
    print(1, s.getProducts()[0].getId())
    s.editProductName('1', 'banana')
    s.editProductOriginalPrice('1','er')

"""
    for p in s.products:
        print(' pid', p.getId())
        for batch in p.getBatches():
            print('bid', batch.getBatchID(), 'acPrice', batch.getActualPrice(), 'quantity', batch.getQuantity())
    for c in s.customers:
        print('id', c.getId())
        print('ShoppingCart', c.getShoppingCart().productsInCart)

    for cid in s.orderHistory:
        for order in s.orderHistory[cid]:
            print(order.getTotalPrice())
            print(order.getTransactionDate())
    #s.writeStore()
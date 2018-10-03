import ShoppingCart
import datetime


class Order:
    # param: orderId, customerId, shoppingCart, totalPrice, transactionDate
    def __init__(self, oId=' ', cId=' ', sCart=None, tPrice=0.0, tDate=datetime.datetime.now()):
        self.customerId = cId
        self.orderId = oId
        self.totalPrice = tPrice
        self.shoppingCart = sCart
        self.transactionDate = tDate

    def getCustomerId(self):
        return self.customerId

    def getOrderId(self):
        return self.orderId

    def getTotalPrice(self):
        return self.totalPrice

    def getShoppingCart(self):
        return self.shoppingCart

    def getTransactionDate(self):
        return self.transactionDate

    def setCustomerId(self, cId=''):
        self.customerId = cId

    def setOrderId(self, oId=''):
        self.orderId = oId

    def setTotalPrice(self, tPrice=0.0):
        self.totalPrice = tPrice

    def setShoppingCart(self, sCart=None):
        self.shoppingCart = sCart

    def setTransactionDate(self, tDate=datetime.datetime.now()):
        self.transactionDate = tDate



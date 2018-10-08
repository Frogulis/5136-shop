
class ShoppingCart:

    # item = [productId, actualPrice, quantity]
    def __init__(self):
        self.productsInCart = []

    def addTupleToShoppingCart(self, itemToBeAdded):
        self.productsInCart.append(itemToBeAdded)

    def addToShoppingCart(self, productId, actualPrice, quantity):
        #self._convertToFloat(actualPrice)
        #self._convertToFloat(quantity)
        newTuple = [productId, round(actualPrice,2), quantity]
        self.productsInCart.append(newTuple)

    def adjustQuantity(self, productId, actualPrice, newQuantity):
        actualPrice = self._convertToFloat(actualPrice)
        found = False
        for item in self.productsInCart:
            if item[0] == productId and item[1] == actualPrice:
                item[2] = newQuantity
                found = True
        if not found:
            raise Exception("Either Product Id or Actual Price is invalid.")

    def _convertToFloat(self, integer):
        try:
            floated = round(float(integer), 2)
        except Exception:
            raise Exception("Parameter should be a float or integer.")
        return floated

    # def deleteFromShoppingCart(self, itemToBeDeleted):
    #    for i in range(len(self.productsInCart)):
    #        if self.productsInCart[i] == itemToBeDeleted:
    #            del self.productsInCart[i]

    # def deleteFromShoppingCart(self, productId, actualPrice = 0.00):
    #    actualPrice = self._convertToFloat(actualPrice)
    def deleteFromShoppingCart(self, productId, actualPrice):
        found = False
        for i in range(len(self.productsInCart) - 1):
            item = self.productsInCart[i]
            if item[0] == productId and item[1] == actualPrice:
                del self.productsInCart[i]
                found = True
        if not found:
            raise Exception("Product Id or Actual Price is invalid.")

    # To get one particular product item
    def getProductInCart(self, productId):
        for item in self.productsInCart:
            if productId == item[0]:
                return item
        raise Exception("Product Id is invalid.")

    def getProductsInCart(self):
        return self.productsInCart

    # To get the total price of the shopping cart.
    def getTotalPrice(self):
        totalPrice = 0.00
        for item in self.productsInCart:
            singlePrice = item[1] * item[2]
            totalPrice += singlePrice
        return round(totalPrice,2)

    def setProductsInCart(self, newList):
        self.productsInCart = newList

# ignore - these are test calls   (ML)
if __name__ == '__main__':
    # productsInCart = [('20010', 3.80, 2), ('20011', 2.90, 4)]
    sCart = ShoppingCart()
    # sCart.setProductsInCart([['20001', 1.50, 4], ['20013', 3.89, 10]])
    sCart.addToShoppingCart('20001', 1.50, 4)
    sCart.addToShoppingCart('20013', 3.89, 10)
    print(sCart.getProductsInCart())
    sCart.addToShoppingCart('20010', 3.80, 2)
    print(sCart.getProductsInCart())
    sCart.addToShoppingCart('200230', 4.99, 1.8943536)
    print(sCart.getProductsInCart())
    sCart.adjustQuantity('20010',5.5)
    print(sCart.getProductsInCart())
    sCart.deleteFromShoppingCart('20001')
    print(sCart.getProductsInCart())
    print(sCart.getProductInCart('200230'))
    print(sCart.getTotalPrice())


